import math
from typing import Dict, Any, List, Optional
from app.config import (
    ONION_SIZE_SMALL_MAX_MM,
    ONION_SIZE_MEDIUM_MAX_MM,
)

class OnionSizeEstimator:
    """
    Physical Metric & Relative Size Estimation Service.
    Converts 2D bounding boxes into physical millimeter diameter when an ArUco scale is calibrated.
    Strictly preserves null for physical millimeters when uncalibrated, with clean relative fallback.
    """
    def __init__(
        self,
        small_max_mm: float = ONION_SIZE_SMALL_MAX_MM,
        medium_max_mm: float = ONION_SIZE_MEDIUM_MAX_MM,
        relative_undersized_threshold: float = 0.65,
        relative_oversized_threshold: float = 1.35
    ):
        self.small_max_mm = small_max_mm
        self.medium_max_mm = medium_max_mm
        self.relative_undersized_threshold = relative_undersized_threshold
        self.relative_oversized_threshold = relative_oversized_threshold

    def estimate_size(
        self,
        bbox: List[int],
        area: float,
        calibration_info: Optional[Dict[str, Any]] = None,
        median_batch_area: float = 1000.0
    ) -> Dict[str, Any]:
        """
        Estimates size for an individual detected onion.
        Returns physical diameter in mm if calibrated, otherwise returns structured relative size.
        """
        x1, y1, x2, y2 = bbox
        bw = max(1, x2 - x1)
        bh = max(1, y2 - y1)

        # Caliper diameter in pixels: average of major and minor bounding-box axes
        diameter_px = float((bw + bh) / 2.0)

        is_calibrated = bool(
            calibration_info and
            calibration_info.get("is_calibrated") and
            calibration_info.get("pixels_per_mm") and
            calibration_info["pixels_per_mm"] > 0
        )

        size_ratio = float(area / median_batch_area) if median_batch_area > 0 else 1.0

        if is_calibrated:
            pixels_per_mm = float(calibration_info["pixels_per_mm"])
            physical_diameter_mm = round(float(diameter_px / pixels_per_mm), 1)

            if physical_diameter_mm < self.small_max_mm:
                size_category = "Small"
                relative_size = "small"
                is_undersized = True
                reason = f"Physical diameter ({physical_diameter_mm}mm) is < {self.small_max_mm}mm procurement minimum"
            elif physical_diameter_mm <= self.medium_max_mm:
                size_category = "Medium"
                relative_size = "medium"
                is_undersized = False
                reason = f"Physical diameter ({physical_diameter_mm}mm) meets standard table onion spec ({self.small_max_mm}-{self.medium_max_mm}mm)"
            else:
                size_category = "Large"
                relative_size = "large"
                is_undersized = False
                reason = f"Physical diameter ({physical_diameter_mm}mm) exceeds {self.medium_max_mm}mm (Jumbo class)"

            return {
                "physical_diameter_mm": physical_diameter_mm,
                "diameter_pixels": round(diameter_px, 1),
                "size_category": size_category,
                "relative_size": relative_size,
                "is_undersized": is_undersized,
                "measurement_status": "calibrated",
                "size_reason": reason,
                "scale_pixels_per_mm": round(pixels_per_mm, 2)
            }
        else:
            # Uncalibrated Fallback: Never fabricate physical millimeters
            if size_ratio < self.relative_undersized_threshold:
                size_category = "Small (Relative)"
                relative_size = "small"
                is_undersized = True
                reason = f"Relative area is < {int(self.relative_undersized_threshold*100)}% of batch median (Uncalibrated)"
            elif size_ratio > self.relative_oversized_threshold:
                size_category = "Large (Relative)"
                relative_size = "large"
                is_undersized = False
                reason = f"Relative area is > {int(self.relative_oversized_threshold*100)}% of batch median (Uncalibrated)"
            else:
                size_category = "Medium (Relative)"
                relative_size = "medium"
                is_undersized = False
                reason = "Within standard batch median distribution (Uncalibrated)"

            return {
                "physical_diameter_mm": None,
                "diameter_pixels": round(diameter_px, 1),
                "size_category": size_category,
                "relative_size": relative_size,
                "is_undersized": is_undersized,
                "measurement_status": "unavailable",
                "size_reason": reason,
                "scale_pixels_per_mm": None
            }

    def summarize_batch(self, size_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Summarizes size metrics across a batch of onions."""
        if not size_items:
            return {
                "calibration_status": "unavailable",
                "counts_by_category": {"Small": 0, "Medium": 0, "Large": 0},
                "mean_diameter_mm": None,
                "undersized_count": 0
            }

        counts = {"Small": 0, "Medium": 0, "Large": 0}
        diameters = []
        is_calibrated = False

        for item in size_items:
            cat = item.get("size_category", "Medium")
            # Normalize category string
            base_cat = "Small" if "Small" in cat else ("Large" if "Large" in cat else "Medium")
            counts[base_cat] += 1

            if item.get("measurement_status") == "calibrated" and item.get("physical_diameter_mm") is not None:
                diameters.append(float(item["physical_diameter_mm"]))
                is_calibrated = True

        mean_dia = round(float(sum(diameters) / len(diameters)), 1) if diameters else None

        return {
            "calibration_status": "calibrated" if is_calibrated else "uncalibrated_relative",
            "counts_by_category": counts,
            "mean_diameter_mm": mean_dia,
            "undersized_count": counts["Small"]
        }
