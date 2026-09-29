import os
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional

from app.services.detector.base_detector import BaseOnionDetector
from app.services.detector.cv_detector import CVOnionDetector
from app.services.calibration.aruco_calibrator import ArucoCalibrator
from app.services.size.size_estimator import OnionSizeEstimator
from app.utils.image_processing import crop_and_save, draw_detection_annotations
from app.config import (
    UPLOAD_DIR,
    ROBOFLOW_API_KEY,
    ROBOFLOW_MODEL_ID,
    ROBOFLOW_API_URL,
    ROBOFLOW_CONFIDENCE,
)

try:
    from inference_sdk import InferenceHTTPClient, InferenceConfiguration
    HAS_INFERENCE_SDK = True
except ImportError:
    HAS_INFERENCE_SDK = False


class RoboflowOnionDetector(BaseOnionDetector):
    """
    Roboflow Serverless Object Detection Integration.
    Uses Roboflow Cloud API with header-based authorization to detect onion objects and disease patterns.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_id: Optional[str] = None,
        api_url: Optional[str] = None,
        conf_threshold: Optional[float] = None
    ):
        self.api_key = api_key or ROBOFLOW_API_KEY
        self.model_id = model_id or ROBOFLOW_MODEL_ID
        self.api_url = api_url or ROBOFLOW_API_URL
        self.conf_threshold = conf_threshold if conf_threshold is not None else ROBOFLOW_CONFIDENCE
        self.cv_fallback = CVOnionDetector()
        self.calibrator = ArucoCalibrator()
        self.size_estimator = OnionSizeEstimator()
        self.client = None

        if HAS_INFERENCE_SDK and self.api_key:
            try:
                # Configure client with header-based authentication as required
                self.client = InferenceHTTPClient(
                    api_url=self.api_url,
                    api_key=self.api_key
                ).configure(InferenceConfiguration(
                    api_key_transport="header"
                ))
            except Exception as e:
                print(f"[Roboflow Detector] Failed to configure client: {e}")
                self.client = None
        else:
            if not self.api_key:
                print("[Roboflow Detector] Warning: ROBOFLOW_API_KEY is not set.")

    def infer_raw(self, image_path_or_url: str, model_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Runs direct inference on an image via Roboflow Serverless API.
        Accepts local file path or image URL.
        """
        if not self.client:
            raise RuntimeError(
                "Roboflow client is not configured. Please ensure ROBOFLOW_API_KEY is set in environment."
            )
        p = Path(image_path_or_url)
        target = str(p.resolve()) if p.exists() else image_path_or_url
        target_model = model_id or self.model_id
        return self.client.infer(target, model_id=target_model)

    def detect(self, image_path: str, upload_id: str) -> dict:
        """
        Detects onions and disease defects using Roboflow Serverless API,
        crops individual items, generates annotations, and returns structured result.
        """
        img_path = Path(image_path)
        if not img_path.exists():
            raise FileNotFoundError(f"Image not found at path: {image_path}")

        img = cv2.imread(str(img_path))
        if img is None:
            raise ValueError(f"Could not load image file: {image_path}")

        # ArUco Metric Reference Calibration
        calibration_info = self.calibrator.detect_marker(img)

        h, w = img.shape[:2]

        # If client not configured, fall back to CV detector
        if not self.client:
            print("[Roboflow Detector] Client unavailable, falling back to CV detector.")
            res = self.cv_fallback.detect(image_path, upload_id)
            res["detector_used"] = "CV Content Detector (Roboflow Client Unconfigured)"
            return res

        # Run inference via Roboflow
        try:
            raw_response = self.infer_raw(str(img_path))
            raw_preds = raw_response.get("predictions", [])
        except Exception as e:
            print(f"[Roboflow Detector] Inference failed: {e}. Running CV fallback.")
            res = self.cv_fallback.detect(image_path, upload_id)
            res["detector_used"] = f"CV Fallback (Roboflow Error: {str(e)[:50]})"
            return res

        onions = []
        raw_boxes = []
        metrics = {
            "total_candidates": len(raw_preds),
            "rejected_by_area": 0,
            "rejected_by_shape": 0,
            "rejected_by_color": 0,
            "rejected_by_confidence": 0,
            "final_detections": 0
        }

        idx_counter = 1
        for pred in raw_preds:
            conf = float(pred.get("confidence", 0.0))
            if conf < self.conf_threshold:
                metrics["rejected_by_confidence"] += 1
                continue

            cx = float(pred.get("x", 0))
            cy = float(pred.get("y", 0))
            bw = float(pred.get("width", 0))
            bh = float(pred.get("height", 0))

            x1 = max(0, int(cx - bw / 2))
            y1 = max(0, int(cy - bh / 2))
            x2 = min(w, int(cx + bw / 2))
            y2 = min(h, int(cy + bh / 2))

            box_w = x2 - x1
            box_h = y2 - y1
            area = float(box_w * box_h)

            if area < 50:
                metrics["rejected_by_area"] += 1
                continue

            bbox = [x1, y1, x2, y2]
            raw_boxes.append([x1, y1, box_w, box_h])

            class_name = pred.get("class", "onion")
            label = f"{class_name.capitalize()} #{idx_counter}"
            crop_path = crop_and_save(img, bbox, upload_id, idx_counter)

            onions.append({
                "id": idx_counter,
                "label": label,
                "bbox": bbox,
                "confidence": round(conf, 2),
                "crop_path": crop_path,
                "area": area,
                "center": [int(cx), int(cy)]
            })
            idx_counter += 1

        metrics["final_detections"] = len(onions)

        # Hybrid ensemble: Roboflow onion-disease/3 is optimized for isolated single onions / lesion detection.
        # If Roboflow yields 0 detections (e.g. dense multi-onion trays or conveyor domain shift), query CV detector.
        if len(onions) == 0:
            print(f"[Roboflow Detector] 0 detections from Roboflow for {img_path.name}. Querying CV fallback.")
            cv_res = self.cv_fallback.detect(image_path, upload_id)
            if cv_res.get("total_onions", 0) > 0:
                cv_res["detector_used"] = f"Hybrid Roboflow ({self.model_id}) + CV Fallback"
                return cv_res

        # Estimate physical or relative size for each onion
        areas = [o["area"] for o in onions]
        median_area = float(np.median(areas)) if areas else 1000.0
        for o in onions:
            o["size"] = self.size_estimator.estimate_size(o["bbox"], o["area"], calibration_info, median_area)

        # Draw annotated detection image (including ArUco marker overlay if present)
        annotated_img = draw_detection_annotations(img, onions, calibration_info)
        annotated_filename = f"{upload_id}_annotated.jpg"
        annotated_file_path = UPLOAD_DIR / annotated_filename
        cv2.imwrite(str(annotated_file_path), annotated_img)

        return {
            "upload_id": upload_id,
            "total_onions": len(onions),
            "annotated_image_url": f"/uploads/{annotated_filename}",
            "onions": onions,
            "raw_boxes": raw_boxes,
            "detector_used": f"Roboflow Serverless Detector ({self.model_id})",
            "calibration": calibration_info,
            "debug_metrics": metrics,
            "status": "success"
        }
