from pydantic import BaseModel
from typing import Dict, List, Optional
from app.schemas.detection import CalibrationInfo, OnionSizeItem

class OnionClassificationItem(BaseModel):
    onion_id: int
    label: str
    class_label: str  # Healthy, Damaged, Rotten, Sprouted, Undersized
    confidence: float
    probabilities: Dict[str, float]
    crop_path: str
    is_defective: bool
    defect_reason: Optional[str] = None
    size: Optional[OnionSizeItem] = None

class BatchClassificationResult(BaseModel):
    upload_id: str
    total_onions: int
    classifications: List[OnionClassificationItem]
    classifier_used: str
    is_demo_mode: bool
    calibration: Optional[CalibrationInfo] = None
    status: str
