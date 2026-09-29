import os
import cv2
import numpy as np
from pathlib import Path
from app.services.detector.base_detector import BaseOnionDetector
from app.services.detector.cv_detector import CVOnionDetector
from app.utils.image_processing import crop_and_save, draw_detection_annotations
from app.config import (
    UPLOAD_DIR,
    DEBUG_DIR,
    ONION_DETECTOR_MODEL,
    DETECTOR_MODE,
    CONFIDENCE_THRESHOLD,
    IOU_THRESHOLD,
    MIN_ONION_AREA_PIXELS,
    MAX_ONION_AREA_RATIO,
    DEBUG_SAVE_PIPELINE
)

try:
    from ultralytics import YOLO
    HAS_ULTRALYTICS = True
except ImportError:
    HAS_ULTRALYTICS = False

class YOLOOnionDetector(BaseOnionDetector):
    """
    YOLO Agricultural Produce Object Detector.
    Detects single target object class: 'onion'.
    Outputs tight bounding boxes [x1, y1, x2, y2] and confidence scores.
    Supports PyTorch weights (.pt) and ONNX models configured via ONION_DETECTOR_MODEL.
    """
    def __init__(
        self,
        model_path: str = ONION_DETECTOR_MODEL,
        conf_threshold: float = CONFIDENCE_THRESHOLD,
        iou_threshold: float = IOU_THRESHOLD
    ):
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.cv_fallback = CVOnionDetector()
        self.model_loaded = False
        self.model = None

        if HAS_ULTRALYTICS and os.path.exists(self.model_path):
            try:
                self.model = YOLO(self.model_path)
                self.model_loaded = True
                print(f"[YOLO Detector] Successfully loaded YOLO model weights from: {self.model_path}")
            except Exception as e:
                print(f"[YOLO Detector Warning] Could not load model from {self.model_path}: {e}")
                self.model_loaded = False

    def detect(self, image_path: str, upload_id: str) -> dict:
        img_path = Path(image_path)
        if not img_path.exists():
            raise FileNotFoundError(f"Image not found at path: {image_path}")

        img = cv2.imread(str(img_path))
        if img is None:
            raise ValueError(f"Could not load image file: {image_path}")

        h, w, c = img.shape
        img_area = h * w
        max_area = img_area * MAX_ONION_AREA_RATIO

        # If trained .pt / .onnx file is not found, execute CV detector (genuine image content analysis)
        if not self.model_loaded:
            if DETECTOR_MODE == "real":
                print(f"[YOLO Detector] Trained model file '{self.model_path}' not present. Running OpenCV image-content segmentation detector.")
            result = self.cv_fallback.detect(image_path, upload_id)
            result["detector_used"] = f"YOLO Onion Detector Engine (CV Content Detector Fallback - {self.model_path} pending)"
            return result

        # Execute YOLO Inference
        results = self.model(img, conf=self.conf_threshold, iou=self.iou_threshold, verbose=False)
        
        raw_boxes = []
        raw_confidences = []
        metrics = {
            "total_candidates": 0,
            "rejected_by_area": 0,
            "rejected_by_shape": 0,
            "rejected_by_color": 0,
            "rejected_by_confidence": 0,
            "final_detections": 0
        }

        if results and len(results) > 0:
            boxes_data = results[0].boxes
            metrics["total_candidates"] = len(boxes_data)

            for box in boxes_data:
                conf = float(box.conf[0])
                if conf < self.conf_threshold:
                    metrics["rejected_by_confidence"] += 1
                    continue

                xyxy = box.xyxy[0].cpu().numpy()
                x1 = max(0, int(xyxy[0]))
                y1 = max(0, int(xyxy[1]))
                x2 = min(w, int(xyxy[2]))
                y2 = min(h, int(xyxy[3]))
                bw = x2 - x1
                bh = y2 - y1
                area = bw * bh

                if area < MIN_ONION_AREA_PIXELS or area > max_area:
                    metrics["rejected_by_area"] += 1
                    continue

                raw_boxes.append([x1, y1, bw, bh])
                raw_confidences.append(conf)

        # Apply Non-Maximum Suppression (NMS) for duplicate removal
        final_onions = []
        if len(raw_boxes) > 0:
            indices = cv2.dnn.NMSBoxes(raw_boxes, raw_confidences, self.conf_threshold, self.iou_threshold)
            if len(indices) > 0:
                indices_list = indices.flatten() if isinstance(indices, np.ndarray) else indices
                for idx_order, idx in enumerate(indices_list, start=1):
                    b = raw_boxes[idx]
                    x1, y1, bw, bh = b
                    x2 = x1 + bw
                    y2 = y1 + bh
                    conf = round(float(raw_confidences[idx]), 2)
                    bbox = [x1, y1, x2, y2]

                    crop_path = crop_and_save(img, bbox, upload_id, idx_order)
                    label = f"Onion #{idx_order}"

                    final_onions.append({
                        "id": idx_order,
                        "label": label,
                        "bbox": bbox,
                        "confidence": conf,
                        "crop_path": crop_path,
                        "area": float(bw * bh),
                        "center": [x1 + bw // 2, y1 + bh // 2]
                    })

        metrics["final_detections"] = len(final_onions)

        # Debug image output
        if DEBUG_SAVE_PIPELINE:
            try:
                cv2.imwrite(str(DEBUG_DIR / f"{upload_id}_1_original.jpg"), img)
                final_debug_img = draw_detection_annotations(img, final_onions)
                cv2.imwrite(str(DEBUG_DIR / f"{upload_id}_6_final_detections.jpg"), final_debug_img)
            except Exception:
                pass

        # Render Final Annotated Image
        annotated_img = draw_detection_annotations(img, final_onions)
        annotated_filename = f"{upload_id}_annotated.jpg"
        annotated_file_path = UPLOAD_DIR / annotated_filename
        cv2.imwrite(str(annotated_file_path), annotated_img)

        return {
            "upload_id": upload_id,
            "total_onions": len(final_onions),
            "annotated_image_url": f"/uploads/{annotated_filename}",
            "onions": final_onions,
            "raw_boxes": raw_boxes,
            "detector_used": f"YOLO Real-Time Object Detector ({self.model_path})",
            "debug_metrics": metrics,
            "status": "success"
        }
