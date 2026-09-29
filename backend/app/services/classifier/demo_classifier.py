import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Any
from app.services.classifier.base_classifier import BaseOnionClassifier
from app.services.feature_extraction import extract_onion_features
from app.services.size.size_estimator import OnionSizeEstimator
from app.config import BASE_DIR, UPLOAD_DIR

class DemoOnionClassifier(BaseOnionClassifier):
    """
    Onion Defect Classifier Engine.
    Uses deterministic CV feature extraction (color, sprout greenness, rot darkness, surface cuts,
    and verified physical diameter or relative area fallback) to classify onions into the 5 target classes.
    """
    def __init__(self, undersized_threshold: float = 0.65):
        self.undersized_threshold = undersized_threshold
        self.size_estimator = OnionSizeEstimator(relative_undersized_threshold=undersized_threshold)

    def classify_batch(
        self,
        onions: List[Dict],
        upload_id: str,
        calibration: Optional[Dict[str, Any]] = None
    ) -> Dict:
        if not onions:
            return {
                "upload_id": upload_id,
                "total_onions": 0,
                "classifications": [],
                "classifier_used": "DEMO_CV_FEATURE_CLASSIFIER",
                "is_demo_mode": True,
                "calibration": calibration,
                "status": "success"
            }

        # Calculate median area across all detected onions in batch
        areas = [item.get("area", 1000.0) for item in onions]
        median_area = float(np.median(areas)) if areas else 1000.0

        results = []
        for onion in onions:
            crop_rel_path = onion.get("crop_path", "")
            onion_id = onion.get("id", 1)
            label = onion.get("label", f"Onion #{onion_id}")
            area = float(onion.get("area", 1000.0))
            bbox = onion.get("bbox", [0, 0, 100, 100])

            # Resolve crop file path
            crop_abs_path = BASE_DIR / crop_rel_path.lstrip("/")
            if not crop_abs_path.exists():
                crop_abs_path = UPLOAD_DIR / "crops" / Path(crop_rel_path).name

            features = {"is_undersized": False, "is_sprouted": False, "is_rotten": False, "is_damaged": False}
            if crop_abs_path.exists():
                crop_img = cv2.imread(str(crop_abs_path))
                if crop_img is not None:
                    features = extract_onion_features(crop_img, area, median_area)
                else:
                    features["is_undersized"] = (area / median_area) < self.undersized_threshold
            else:
                features["is_undersized"] = (area / median_area) < self.undersized_threshold

            # Size estimation: use existing size object if attached, or estimate now
            size_data = onion.get("size")
            if not size_data:
                size_data = self.size_estimator.estimate_size(bbox, area, calibration, median_area)

            # Sizing override: if physical calibration is available, rely on physical diameter threshold
            if size_data.get("measurement_status") == "calibrated":
                features["is_undersized"] = size_data.get("is_undersized", False)
                size_reason = size_data.get("size_reason", "")
            else:
                features["is_undersized"] = size_data.get("is_undersized", (area / median_area) < self.undersized_threshold)
                size_reason = size_data.get("size_reason", f"Onion relative area ({int(area)}) is < 65% of batch median")

            # Determine dominant class & probability distribution
            if features["is_undersized"]:
                class_label = "Undersized"
                probs = {"Healthy": 0.05, "Damaged": 0.03, "Rotten": 0.02, "Sprouted": 0.02, "Undersized": 0.88}
                reason = size_reason
            elif features["is_sprouted"]:
                class_label = "Sprouted"
                probs = {"Healthy": 0.04, "Damaged": 0.03, "Rotten": 0.03, "Sprouted": 0.88, "Undersized": 0.02}
                reason = "Visible green sprout foliage detected at top node"
            elif features["is_rotten"]:
                class_label = "Rotten"
                probs = {"Healthy": 0.03, "Damaged": 0.05, "Rotten": 0.87, "Sprouted": 0.02, "Undersized": 0.03}
                reason = "Significant dark rot/decay patch identified on outer scale"
            elif features["is_damaged"]:
                class_label = "Damaged"
                probs = {"Healthy": 0.08, "Damaged": 0.82, "Rotten": 0.05, "Sprouted": 0.02, "Undersized": 0.03}
                reason = "Mechanical cut / surface crack pattern detected"
            else:
                class_label = "Healthy"
                probs = {"Healthy": 0.92, "Damaged": 0.03, "Rotten": 0.02, "Sprouted": 0.02, "Undersized": 0.01}
                reason = "Uniform shape, healthy skin color, no visible defects"

            confidence = float(probs[class_label])
            is_defective = (class_label != "Healthy")

            results.append({
                "onion_id": onion_id,
                "label": label,
                "class_label": class_label,
                "confidence": confidence,
                "probabilities": probs,
                "crop_path": crop_rel_path,
                "is_defective": is_defective,
                "defect_reason": reason,
                "size": size_data
            })

        return {
            "upload_id": upload_id,
            "total_onions": len(results),
            "classifications": results,
            "classifier_used": "DEMO_CV_FEATURE_CLASSIFIER",
            "is_demo_mode": True,
            "calibration": calibration,
            "status": "success"
        }
