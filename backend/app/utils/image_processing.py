import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
from app.config import UPLOAD_DIR

CROPS_DIR = UPLOAD_DIR / "crops"
CROPS_DIR.mkdir(parents=True, exist_ok=True)

def crop_and_save(image: np.ndarray, bbox: tuple[int, int, int, int], upload_id: str, onion_id: int) -> str:
    """
    Crops onion region from image given bbox [x1, y1, x2, y2], adds padding,
    saves crop image file, and returns relative access URL path.
    """
    h, w = image.shape[:2]
    x1, y1, x2, y2 = bbox

    # Add 5% padding around crop
    bw = x2 - x1
    bh = y2 - y1
    pad_x = int(bw * 0.05)
    pad_y = int(bh * 0.05)

    px1 = max(0, x1 - pad_x)
    py1 = max(0, y1 - pad_y)
    px2 = min(w, x2 + pad_x)
    py2 = min(h, y2 + pad_y)

    crop = image[py1:py2, px1:px2]
    if crop.size == 0:
        crop = image[y1:y2, x1:x2]

    crop_filename = f"{upload_id}_crop_{onion_id}.jpg"
    crop_file_path = CROPS_DIR / crop_filename

    # Save RGB crop using OpenCV
    cv2.imwrite(str(crop_file_path), crop)
    return f"/uploads/crops/{crop_filename}"

def draw_detection_annotations(
    image: np.ndarray,
    detections: List[Dict],
    calibration_info: Optional[Dict] = None
) -> np.ndarray:
    """
    Draws professional bounding boxes, numbered badge tags, physical diameter/relative size,
    and ArUco marker calibration overlays.
    """
    annotated = image.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX

    # 1. If Calibrated, draw ArUco Reference Marker Overlay
    if calibration_info and calibration_info.get("is_calibrated") and calibration_info.get("marker_corners"):
        corners = np.array(calibration_info["marker_corners"], dtype=np.int32)
        cv2.polylines(annotated, [corners], isClosed=True, color=(0, 255, 200), thickness=2)
        for pt in corners:
            cv2.circle(annotated, tuple(pt), 4, (0, 200, 255), -1)

        px_mm = calibration_info["pixels_per_mm"]
        m_id = calibration_info.get("marker_id", 0)
        ref_mm = calibration_info.get("reference_width_mm", 50.0)
        cx = int(calibration_info["marker_center"][0])
        cy = int(calibration_info["marker_center"][1])

        marker_label = f"Ref ArUco #{m_id} [{px_mm:.2f} px/mm | {ref_mm}mm]"
        (mw, mh), _ = cv2.getTextSize(marker_label, font, 0.45, 1)
        tx = max(10, min(image.shape[1] - mw - 15, cx - mw // 2))
        ty = max(20, cy - 20)
        cv2.rectangle(annotated, (tx - 4, ty - mh - 4), (tx + mw + 4, ty + 4), (15, 20, 25), -1)
        cv2.putText(annotated, marker_label, (tx, ty), font, 0.45, (0, 255, 200), 1, cv2.LINE_AA)
    elif calibration_info and not calibration_info.get("is_calibrated"):
        # Draw small uncalibrated watermark
        uncal_text = "Ref Marker Not Detected (Relative Sizing Active)"
        (uw, uh), _ = cv2.getTextSize(uncal_text, font, 0.45, 1)
        cv2.rectangle(annotated, (10, 10), (20 + uw, 20 + uh + 6), (20, 20, 30), -1)
        cv2.putText(annotated, uncal_text, (15, 22 + uh), font, 0.45, (80, 180, 255), 1, cv2.LINE_AA)

    # 2. Draw Onion Bounding Boxes & Badges
    for item in detections:
        x1, y1, x2, y2 = item["bbox"]
        label = item["label"]
        
        # Check size annotation
        size_info = item.get("size")
        if size_info and size_info.get("physical_diameter_mm") is not None:
            dia_mm = size_info["physical_diameter_mm"]
            cat = size_info.get("size_category", "")
            badge_text = f"{label} | {dia_mm}mm ({cat})"
        elif size_info and size_info.get("size_category"):
            badge_text = f"{label} | {size_info['size_category']}"
        else:
            badge_text = label

        # Box color (Emerald green)
        box_color = (46, 175, 110)
        cv2.rectangle(annotated, (x1, y1), (x2, y2), box_color, 2)

        font_scale = 0.5
        thickness = 1
        (text_w, text_h), baseline = cv2.getTextSize(badge_text, font, font_scale, thickness)
        
        badge_y1 = max(0, y1 - text_h - 8)
        badge_y2 = y1
        badge_x1 = x1
        badge_x2 = min(image.shape[1], x1 + text_w + 10)

        cv2.rectangle(annotated, (badge_x1, badge_y1), (badge_x2, badge_y2), (25, 30, 35), -1)
        cv2.rectangle(annotated, (badge_x1, badge_y1), (badge_x2, badge_y2), box_color, 1)
        cv2.putText(
            annotated,
            badge_text,
            (x1 + 4, y1 - 5),
            font,
            font_scale,
            (255, 255, 255),
            thickness,
            cv2.LINE_AA
        )

    return annotated
