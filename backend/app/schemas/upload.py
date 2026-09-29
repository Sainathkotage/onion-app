from pydantic import BaseModel

class UploadResponse(BaseModel):
    upload_id: str
    filename: str
    original_filename: str
    width: int
    height: int
    format: str
    status: str
    access_url: str
