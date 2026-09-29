from app.services.detector.base_detector import BaseOnionDetector
from app.services.detector.gemini_detector import GeminiOnionDetector
from app.services.detector.cv_detector import CVOnionDetector
from app.services.detector.yolo_detector import YOLOOnionDetector
from app.services.detector.yolo_odd_detector import YOLOODDOnionDetector
from app.services.detector.roboflow_detector import RoboflowOnionDetector
from app.config import DETECTOR_MODE, ONION_DETECTOR_MODEL, GEMINI_API_KEY, SUPPRESS_OTHER_MODELS

class OnionDetectorFactory:
    """
    Factory service for instantiating onion detectors.
    Prioritizes Google Gemini Vision for counting and detection,
    while suppressing other legacy ML models (YOLO, Roboflow, CV).
    """
    @staticmethod
    def get_detector(detector_type: str = None) -> BaseOnionDetector:
        # If other models are suppressed or Gemini API key is available, use Gemini
        if SUPPRESS_OTHER_MODELS or detector_type in ["gemini", "gemini_vision", "google"]:
            return GeminiOnionDetector()

        if detector_type is None:
            if GEMINI_API_KEY:
                detector_type = "gemini"
            elif os.getenv("ROBOFLOW_API_KEY"):
                detector_type = os.getenv("ONION_DETECTOR_TYPE", "roboflow").lower()
            elif os.path.exists(ONION_DETECTOR_MODEL):
                detector_type = os.getenv("ONION_DETECTOR_TYPE", "yolo").lower()
            else:
                detector_type = os.getenv("ONION_DETECTOR_TYPE", "cv").lower()

        if detector_type in ["gemini", "gemini_vision", "google"]:
            return GeminiOnionDetector()
        elif detector_type in ["roboflow", "rf", "serverless", "roboflow_detector"]:
            return RoboflowOnionDetector()
        elif detector_type in ["yolo", "yolo_detector"]:
            return YOLOOnionDetector(model_path=ONION_DETECTOR_MODEL)
        elif detector_type in ["yolo_odd", "odd"]:
            return YOLOODDOnionDetector()
        elif detector_type in ["cv", "opencv"]:
            return CVOnionDetector()
        else:
            return GeminiOnionDetector()

