import os
import cv2
import json
import base64
import requests
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List
from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    UPLOAD_DIR,
    BASE_DIR
)
from app.utils.image_processing import crop_and_save

# In-memory analysis cache keyed by upload_id
_gemini_cache: Dict[str, Dict[str, Any]] = {}

class GeminiVisionService:
    """
    Google Gemini Multimodal Vision Service for Onion Assessment.
    Provides direct zero-shot object detection (counting, bounding boxes)
    and deep agricultural defect classification / batch grading.
    """

    @classmethod
    def get_cached_analysis(cls, upload_id: str) -> Optional[Dict[str, Any]]:
        return _gemini_cache.get(upload_id)

    @classmethod
    def analyze_image(cls, image_path: str, upload_id: str) -> Dict[str, Any]:
        if upload_id in _gemini_cache:
            return _gemini_cache[upload_id]

        img_p = Path(image_path)
        if not img_p.exists():
            raise FileNotFoundError(f"Image file does not exist: {image_path}")

        # Load image via OpenCV to get dimensions and generate crops
        img = cv2.imread(str(img_p))
        if img is None:
            raise ValueError(f"Could not decode image at {image_path}")
        h, w = img.shape[:2]

        # Base64 encode for Gemini Vision API
        with open(img_p, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")

        api_key = GEMINI_API_KEY
        model = GEMINI_MODEL or "gemini-3.6-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

        prompt = """You are an expert agricultural inspection AI specializing in onion procurement and quality grading.
Carefully examine the provided image of onions:
1. Count the exact total number of individual onions visible.
2. For each onion, locate its 2D bounding box and assess its individual quality and defects.
   - Condition must be one of: ["Healthy", "Damaged", "Rotten", "Sprouted", "Undersized"].
   - Provide a confidence score (0.0 to 1.0) and a brief defect description explaining why it has that condition.
3. Assess the overall batch quality:
   - Provide overall_quality (e.g. "High Quality / Grade A", "Medium Quality", "Low Quality / Rejected").
   - Provide a comprehensive quality_summary paragraph explaining onion counts, freshness, skin integrity, defect rates, and procurement observations.
   - Provide recommendation: one of ["ACCEPT", "RE-INSPECT", "REJECT"].
   - Calculate grade_a_percentage and urs_percentage.

Output strictly valid JSON with this exact schema:
{
  "total_onions": <int count>,
  "overall_quality": "<string>",
  "quality_summary": "<detailed quality assessment paragraph>",
  "grade_a_percentage": <float 0-100>,
  "urs_percentage": <float 0-100>,
  "recommendation": "<ACCEPT / RE-INSPECT / REJECT>",
  "onions": [
    {
      "id": <int 1, 2, ...>,
      "box_2d": [ymin, xmin, ymax, xmax], // normalized integers from 0 to 1000
      "condition": "<Healthy | Damaged | Rotten | Sprouted | Undersized>",
      "confidence": <float 0.0 to 1.0>,
      "defect_description": "<explanation of physical appearance/defect>"
    }
  ]
}
"""

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": img_b64
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "response_mime_type": "application/json"
            }
        }

        try:
            resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=45)
            if resp.status_code != 200:
                raise RuntimeError(f"Gemini API Error (status {resp.status_code}): {resp.text}")

            data = resp.json()
            raw_content = data["candidates"][0]["content"]["parts"][0]["text"]
            result_json = json.loads(raw_content)
        except Exception as e:
            print(f"Gemini API call failed: {e}")
            raise e

        # Process detected onions and generate crops
        raw_onions = result_json.get("onions", [])
        processed_onions = []
        raw_boxes = []

        annotated_img = img.copy()

        # Defect color palette (BGR)
        color_palette = {
            "Healthy": (107, 255, 124),    # Emerald #7CFF6B
            "Damaged": (71, 181, 255),    # Amber/Orange #FFB547
            "Rotten": (92, 92, 255),      # Coral Red #FF5C5C
            "Sprouted": (247, 85, 168),   # Purple #A855F7
            "Undersized": (248, 189, 56)  # Cyan/Sky #38BDF8
        }

        for idx, item in enumerate(raw_onions, start=1):
            oid = item.get("id", idx)
            condition = item.get("condition", "Healthy").capitalize()
            if condition not in color_palette:
                condition = "Healthy"

            confidence = float(item.get("confidence", 0.95))
            defect_desc = item.get("defect_description", f"{condition} condition")
            box_2d = item.get("box_2d", [0, 0, 1000, 1000])

            ymin, xmin, ymax, xmax = box_2d
            x1 = max(0, min(w - 1, int(xmin * w / 1000.0)))
            y1 = max(0, min(h - 1, int(ymin * h / 1000.0)))
            x2 = max(x1 + 1, min(w, int(xmax * w / 1000.0)))
            y2 = max(y1 + 1, min(h, int(ymax * h / 1000.0)))

            bbox = (x1, y1, x2, y2)
            raw_boxes.append([x1, y1, x2, y2])
            area = float((x2 - x1) * (y2 - y1))
            center = (int((x1 + x2) / 2), int((y1 + y2) / 2))

            # Generate individual onion crop image
            crop_rel_url = crop_and_save(img, bbox, upload_id, oid)

            processed_onions.append({
                "id": oid,
                "label": f"Onion #{oid}",
                "bbox": bbox,
                "confidence": round(confidence, 4),
                "crop_path": crop_rel_url,
                "area": area,
                "center": center,
                "condition": condition,
                "defect_description": defect_desc,
                "size": {
                    "physical_diameter_mm": None,
                    "diameter_pixels": round(float(max(x2 - x1, y2 - y1)), 1),
                    "size_category": "Small" if condition == "Undersized" else "Medium",
                    "relative_size": "small" if condition == "Undersized" else "medium",
                    "is_undersized": (condition == "Undersized"),
                    "measurement_status": "unavailable",
                    "size_reason": defect_desc if condition == "Undersized" else "Standard procurement sizing",
                    "scale_pixels_per_mm": None
                }
            })

            # Draw bounding box and badge on annotated image
            color = color_palette.get(condition, (107, 255, 124))
            cv2.rectangle(annotated_img, (x1, y1), (x2, y2), color, 2)

            badge_text = f"#{oid}: {condition} ({int(confidence * 100)}%)"
            font = cv2.FONT_HERSHEY_SIMPLEX
            (tw, th), _ = cv2.getTextSize(badge_text, font, 0.45, 1)

            by1 = max(0, y1 - th - 6)
            by2 = y1
            bx1 = x1
            bx2 = min(w, x1 + tw + 8)

            cv2.rectangle(annotated_img, (bx1, by1), (bx2, by2), (20, 20, 25), -1)
            cv2.rectangle(annotated_img, (bx1, by1), (bx2, by2), color, 1)
            cv2.putText(annotated_img, badge_text, (x1 + 4, max(12, y1 - 4)), font, 0.45, (255, 255, 255), 1, cv2.LINE_AA)

        # Draw Top AI Assessment Watermark
        total_cnt = len(processed_onions)
        overall_q = result_json.get("overall_quality", "Evaluated")
        watermark = f"Gemini 3.6 Flash: {total_cnt} Onions Detected | Quality: {overall_q}"
        (ww, wh), _ = cv2.getTextSize(watermark, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(annotated_img, (10, 10), (16 + ww, 16 + wh + 6), (15, 15, 20), -1)
        cv2.rectangle(annotated_img, (10, 10), (16 + ww, 16 + wh + 6), (107, 255, 124), 1)
        cv2.putText(annotated_img, watermark, (14, 24 + wh), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (107, 255, 124), 1, cv2.LINE_AA)

        # Save annotated image
        annotated_filename = f"{upload_id}_annotated.jpg"
        annotated_path = UPLOAD_DIR / annotated_filename
        cv2.imwrite(str(annotated_path), annotated_img)

        final_result = {
            "upload_id": upload_id,
            "total_onions": total_cnt,
            "annotated_image_url": f"/uploads/{annotated_filename}",
            "onions": processed_onions,
            "raw_boxes": raw_boxes,
            "overall_quality": result_json.get("overall_quality", "Assessed by Gemini"),
            "quality_summary": result_json.get("quality_summary", ""),
            "grade_a_percentage": float(result_json.get("grade_a_percentage", 0.0)),
            "urs_percentage": float(result_json.get("urs_percentage", 0.0)),
            "recommendation": result_json.get("recommendation", "RE-INSPECT"),
            "detector_used": "Google Gemini 3.6 Flash (Vision Multimodal)",
            "status": "success"
        }

        _gemini_cache[upload_id] = final_result
        return final_result
