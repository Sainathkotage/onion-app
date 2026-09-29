from pydantic import BaseModel
from typing import List, Tuple, Optional, Any, Dict

class CalibrationInfo(BaseModel):
    status: str  # "calibrated" | "not_calibrated"
    is_calibrated: bool
    pixels_per_mm: Optional[float] = None
    reference_width_mm: float
    marker_id: Optional[int] = None
    marker_side_pixels: Optional[float] = None
    marker_center: Optional[List[float]] = None
    marker_corners: Optional[List[List[float]]] = None
    distortion_ratio: Optional[float] = None
    perspective_warning: Optional[str] = None
    message: str

class OnionSizeItem(BaseModel):
    physical_diameter_mm: Optional[float] = None
    diameter_pixels: float
    size_category: str  # Small, Medium, Large or Small (Relative), etc.
    relative_size: str  # small, medium, large
    is_undersized: bool
    measurement_status: str  # "calibrated" | "unavailable"
    size_reason: str
    scale_pixels_per_mm: Optional[float] = None

class OnionDetectionItem(BaseModel):
    id: int
    label: str
    bbox: Tuple[int, int, int, int]  # [x1, y1, x2, y2]
    confidence: float
    crop_path: str
    area: float
    center: Tuple[int, int]
    size: Optional[OnionSizeItem] = None

class DetectionDebugMetrics(BaseModel):
    total_candidates: int
    rejected_by_area: int
    rejected_by_shape: int
    rejected_by_color: int
    rejected_by_confidence: int
    final_detections: int

class DetectionResult(BaseModel):
    upload_id: str
    total_onions: int
    annotated_image_url: str
    onions: List[OnionDetectionItem]
    raw_boxes: Optional[List[List[int]]] = None
    detector_used: str
    calibration: Optional[CalibrationInfo] = None
    debug_metrics: DetectionDebugMetrics
    status: str
