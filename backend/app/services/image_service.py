import uuid
import os
from pathlib import Path
from PIL import Image
from fastapi import UploadFile, HTTPException
from app.config import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB

async def save_uploaded_image(file: UploadFile) -> dict:
    try:
        raw_name = Path(file.filename or "image.jpg").name
        ext = Path(raw_name).suffix.lower()
        if not ext:
            ext = ".jpg"
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format '{ext}'. Allowed formats: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            )
        
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty (0 bytes)."
            )
        if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum limit of {MAX_FILE_SIZE_MB}MB"
            )
        
        upload_id = str(uuid.uuid4())
        filename = f"{upload_id}{ext}"
        file_path = UPLOAD_DIR / filename
        
        with open(file_path, "wb") as f:
            f.write(content)
            
        try:
            with Image.open(file_path) as img:
                img.verify()
            with Image.open(file_path) as img:
                width, height = img.size
                format_name = img.format or ext.lstrip(".").upper()
        except Exception:
            if file_path.exists():
                try:
                    os.remove(file_path)
                except OSError:
                    pass
            raise HTTPException(status_code=400, detail="Invalid image file or file corrupted.")
            
        return {
            "upload_id": upload_id,
            "filename": filename,
            "original_filename": raw_name,
            "width": width,
            "height": height,
            "format": format_name,
            "status": "success",
            "access_url": f"/uploads/{filename}"
        }
    finally:
        await file.close()

