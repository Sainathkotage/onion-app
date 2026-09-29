from app.services.detector.base_detector import BaseOnionDetector
from app.services.gemini_service import GeminiVisionService
from app.schemas.detection import DetectionResult, DetectionDebugMetrics, OnionDetectionItem

class GeminiOnionDetector(BaseOnionDetector):
    """
    Google Gemini Multimodal Vision Detector.
    Suppresses legacy ML models (YOLO, Roboflow, CV) and uses Gemini
    for zero-shot detection, counting, and quality assessment.
    """
    def detect(self, image_path: str, upload_id: str) -> DetectionResult:
        result = GeminiVisionService.analyze_image(image_path, upload_id)
        
        onions_items = []
        for o in result.get("onions", []):
            onions_items.append(OnionDetectionItem(
                id=o["id"],
                label=o["label"],
                bbox=o["bbox"],
                confidence=o["confidence"],
                crop_path=o["crop_path"],
                area=o["area"],
                center=o["center"],
                size=o.get("size")
            ))

        debug_metrics = DetectionDebugMetrics(
            total_candidates=result.get("total_onions", 0),
            rejected_by_area=0,
            rejected_by_shape=0,
            rejected_by_color=0,
            rejected_by_confidence=0,
            final_detections=result.get("total_onions", 0)
        )

        return DetectionResult(
            upload_id=upload_id,
            total_onions=result.get("total_onions", len(onions_items)),
            annotated_image_url=result.get("annotated_image_url", ""),
            onions=onions_items,
            raw_boxes=result.get("raw_boxes", []),
            detector_used=result.get("detector_used", "Google Gemini 3.6 Flash (Vision)"),
            calibration=None,
            debug_metrics=debug_metrics,
            status="success"
        )
