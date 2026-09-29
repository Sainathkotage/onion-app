from abc import ABC, abstractmethod

class BaseOnionDetector(ABC):
    """
    Abstract interface for onion detection implementations.
    Allows seamlessly swapping classical CV detectors with trained YOLO/ONNX models.
    """
    @abstractmethod
    def detect(self, image_path: str, upload_id: str) -> dict:
        """
        Input: absolute image_path, upload_id
        Output: dictionary conforming to DetectionResult schema
        """
        pass
