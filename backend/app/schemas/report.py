from pydantic import BaseModel
from typing import List, Optional
from app.schemas.grading import BatchGradingResult
from app.schemas.classification import OnionClassificationItem

class FullAnalysisResponse(BaseModel):
    batch_id: str
    upload_id: str
    timestamp: str
    original_image_url: str
    annotated_image_url: str
    grading: BatchGradingResult
    classifications: List[OnionClassificationItem]
    pdf_report_url: Optional[str] = None
    status: str
