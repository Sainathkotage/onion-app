from datetime import datetime
from typing import List, Dict, Optional, Any
from app.services.grading.grading_rules import ProcurementGradingRules

class OnionGradingService:
    """
    Calculates batch totals, Grade A vs URS percentages, defect breakdowns,
    metric physical size categorization (Small/Medium/Large), and procurement recommendations.
    """
    @staticmethod
    def calculate_grading(
        upload_id: str,
        classifications: List[Dict],
        calibration: Optional[Dict[str, Any]] = None
    ) -> Dict:
        total_onions = len(classifications)
        
        is_calibrated = bool(calibration and calibration.get("is_calibrated"))
        grading_status = "calibrated" if is_calibrated else "uncalibrated_relative"

        if total_onions == 0:
            return {
                "batch_id": f"BATCH-{upload_id[:8].upper()}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_onions": 0,
                "grade_a": {"count": 0, "percentage": 0.0},
                "urs": {"count": 0, "percentage": 0.0},
                "breakdown": {
                    "healthy": {"count": 0, "percentage": 0.0},
                    "damaged": {"count": 0, "percentage": 0.0},
                    "rotten": {"count": 0, "percentage": 0.0},
                    "sprouted": {"count": 0, "percentage": 0.0},
                    "undersized": {"count": 0, "percentage": 0.0},
                },
                "size_breakdown": {
                    "small": {"count": 0, "percentage": 0.0},
                    "medium": {"count": 0, "percentage": 0.0},
                    "large": {"count": 0, "percentage": 0.0},
                    "mean_diameter_mm": None,
                },
                "grading_status": grading_status,
                "calibration": calibration,
                "recommendation": "REJECT (Empty Batch)",
                "status": "success"
            }

        counts = {
            "Healthy": 0,
            "Damaged": 0,
            "Rotten": 0,
            "Sprouted": 0,
            "Undersized": 0
        }

        size_counts = {
            "Small": 0,
            "Medium": 0,
            "Large": 0
        }
        diameters = []

        for item in classifications:
            cls_name = item.get("class_label", "Healthy")
            if cls_name in counts:
                counts[cls_name] += 1
            else:
                counts["Healthy"] += 1

            # Extract size category and physical diameter
            size_obj = item.get("size")
            if size_obj:
                raw_cat = size_obj.get("size_category", "Medium")
                if "Small" in raw_cat:
                    size_counts["Small"] += 1
                elif "Large" in raw_cat:
                    size_counts["Large"] += 1
                else:
                    size_counts["Medium"] += 1

                dia = size_obj.get("physical_diameter_mm")
                if dia is not None:
                    diameters.append(float(dia))
            else:
                if cls_name == "Undersized":
                    size_counts["Small"] += 1
                else:
                    size_counts["Medium"] += 1

        grade_a_count = counts["Healthy"]
        urs_count = counts["Damaged"] + counts["Rotten"] + counts["Sprouted"] + counts["Undersized"]

        grade_a_pct = round((grade_a_count / total_onions) * 100.0, 1)
        urs_pct = round((urs_count / total_onions) * 100.0, 1)

        recommendation = ProcurementGradingRules.get_recommendation(grade_a_pct)

        def make_cp(count: int) -> Dict:
            return {
                "count": count,
                "percentage": round((count / total_onions) * 100.0, 1)
            }

        # Retrieve Gemini quality assessment if available
        from app.services.gemini_service import GeminiVisionService
        cached_gemini = GeminiVisionService.get_cached_analysis(upload_id)
        quality_summary = cached_gemini.get("quality_summary") if cached_gemini else None
        if cached_gemini and cached_gemini.get("recommendation"):
            recommendation = cached_gemini["recommendation"]

        mean_diameter = round(float(sum(diameters) / len(diameters)), 1) if diameters else None

        return {
            "batch_id": f"BATCH-{upload_id[:8].upper()}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_onions": total_onions,
            "grade_a": {"count": grade_a_count, "percentage": grade_a_pct},
            "urs": {"count": urs_count, "percentage": urs_pct},
            "breakdown": {
                "healthy": make_cp(counts["Healthy"]),
                "damaged": make_cp(counts["Damaged"]),
                "rotten": make_cp(counts["Rotten"]),
                "sprouted": make_cp(counts["Sprouted"]),
                "undersized": make_cp(counts["Undersized"]),
            },
            "size_breakdown": {
                "small": make_cp(size_counts["Small"]),
                "medium": make_cp(size_counts["Medium"]),
                "large": make_cp(size_counts["Large"]),
                "mean_diameter_mm": mean_diameter,
            },
            "grading_status": grading_status,
            "calibration": calibration,
            "recommendation": recommendation,
            "quality_summary": quality_summary,
            "ai_engine": "Google Gemini 3.6 Flash",
            "status": "success"
        }
