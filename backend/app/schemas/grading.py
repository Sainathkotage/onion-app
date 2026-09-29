from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from app.schemas.detection import CalibrationInfo

class CountPercentage(BaseModel):
    count: int
    percentage: float

class BreakdownDetail(BaseModel):
    healthy: CountPercentage
    damaged: CountPercentage
    rotten: CountPercentage
    sprouted: CountPercentage
    undersized: CountPercentage

class SizeCategoryBreakdown(BaseModel):
    small: CountPercentage
    medium: CountPercentage
    large: CountPercentage
    mean_diameter_mm: Optional[float] = None

class BatchGradingResult(BaseModel):
    batch_id: str
    timestamp: str
    total_onions: int
    grade_a: CountPercentage
    urs: CountPercentage
    breakdown: BreakdownDetail
    size_breakdown: Optional[SizeCategoryBreakdown] = None
    grading_status: str  # "calibrated" | "uncalibrated_relative"
    calibration: Optional[CalibrationInfo] = None
    recommendation: str  # ACCEPT, RE-INSPECT, REJECT
    quality_summary: Optional[str] = None
    ai_engine: Optional[str] = "Google Gemini 3.6 Flash"
    status: str
