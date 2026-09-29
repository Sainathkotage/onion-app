from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from fastapi.responses import FileResponse
from app.services.image_service import save_uploaded_image
from app.services.detector.detector_factory import OnionDetectorFactory
from app.services.classifier.classifier_factory import OnionClassifierFactory
from app.services.grading.grading_service import OnionGradingService
from app.services.report.report_builder import ReportBuilderService
from app.schemas.detection import DetectionResult
from app.schemas.classification import BatchClassificationResult
from app.schemas.grading import BatchGradingResult
from app.schemas.report import FullAnalysisResponse
from app.schemas.upload import UploadResponse
from app.config import UPLOAD_DIR, BASE_DIR
from pathlib import Path

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "OnionIQ Backend API",
        "version": "1.0.0"
    }

@router.post("/upload", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")
    result = await save_uploaded_image(file)
    return result

@router.post("/analyze/detect", response_model=DetectionResult)
async def detect_onions(payload: dict = Body(...)):
    upload_id = payload.get("upload_id")
    filename = payload.get("filename")

    if not upload_id or not filename:
        raise HTTPException(status_code=400, detail="upload_id and filename are required.")

    image_path = UPLOAD_DIR / filename
    if not image_path.exists():
        raise HTTPException(status_code=404, detail=f"Image file not found for upload_id: {upload_id}")

    detector_type = payload.get("detector_type")

    try:
        detector = OnionDetectorFactory.get_detector(detector_type)
        result = detector.detect(str(image_path), upload_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

@router.post("/roboflow/infer")
async def roboflow_infer(payload: dict = Body(...)):
    """
    Runs direct serverless inference on an image via Roboflow Cloud API.
    Accepts local file path, upload filename, or public image URL.
    """
    image_input = payload.get("image") or payload.get("image_path")
    model_id = payload.get("model_id")

    if not image_input and payload.get("filename"):
        target_path = UPLOAD_DIR / payload["filename"]
        if target_path.exists():
            image_input = str(target_path)

    if not image_input:
        raise HTTPException(status_code=400, detail="'image', 'image_path', or 'filename' is required.")

    try:
        from app.services.detector.roboflow_detector import RoboflowOnionDetector
        detector = RoboflowOnionDetector()
        result = detector.infer_raw(image_input, model_id=model_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Roboflow inference failed: {str(e)}")


@router.post("/analyze/gemini")
async def gemini_analyze_direct(payload: dict = Body(...)):
    """
    Direct endpoint for Gemini Vision multimodal analysis.
    Counts onions, extracts bounding boxes, diagnoses defects, and grades batch quality.
    """
    upload_id = payload.get("upload_id")
    filename = payload.get("filename")

    if not upload_id or not filename:
        raise HTTPException(status_code=400, detail="upload_id and filename are required.")

    image_path = UPLOAD_DIR / filename
    if not image_path.exists():
        raise HTTPException(status_code=404, detail=f"Image file not found for upload_id: {upload_id}")

    try:
        from app.services.gemini_service import GeminiVisionService
        result = GeminiVisionService.analyze_image(str(image_path), upload_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini analysis failed: {str(e)}")


@router.post("/analyze/classify", response_model=BatchClassificationResult)
async def classify_onions(payload: dict = Body(...)):
    upload_id = payload.get("upload_id")
    onions = payload.get("onions", [])
    calibration = payload.get("calibration")

    if not upload_id:
        raise HTTPException(status_code=400, detail="upload_id is required.")

    try:
        classifier = OnionClassifierFactory.get_classifier()
        result = classifier.classify_batch(onions, upload_id, calibration=calibration)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

@router.post("/analyze/grade", response_model=BatchGradingResult)
async def grade_batch(payload: dict = Body(...)):
    """
    Calculates Grade A %, URS %, defect breakdown, physical sizing, and procurement recommendation.
    """
    upload_id = payload.get("upload_id")
    classifications = payload.get("classifications", [])
    calibration = payload.get("calibration")

    if not upload_id:
        raise HTTPException(status_code=400, detail="upload_id is required.")

    try:
        result = OnionGradingService.calculate_grading(upload_id, classifications, calibration=calibration)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Grading calculation failed: {str(e)}")

@router.post("/reports/pdf")
async def generate_pdf_report(payload: dict = Body(...)):
    """
    Generates downloadable PDF report and returns access URL.
    """
    upload_id = payload.get("upload_id")
    grading_result = payload.get("grading")
    classifications = payload.get("classifications", [])
    annotated_image_url = payload.get("annotated_image_url", "")

    if not upload_id or not grading_result:
        raise HTTPException(status_code=400, detail="upload_id and grading result are required.")

    try:
        report_data = ReportBuilderService.build_report(
            grading_result=grading_result,
            classifications=classifications,
            annotated_image_url=annotated_image_url,
            upload_id=upload_id
        )
        return report_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@router.get("/reports/{report_filename}/download")
async def download_pdf_file(report_filename: str):
    """
    Direct endpoint for downloading PDF file.
    """
    pdf_path = UPLOAD_DIR / "reports" / report_filename
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="PDF report file not found.")

    return FileResponse(
        path=str(pdf_path),
        filename=report_filename,
        media_type="application/pdf"
    )

@router.get("/download/app")
@router.get("/download/apk")
async def download_app_apk():
    """
    Direct endpoint for downloading the OnionIQ Mobile Android APK.
    """
    apk_candidates = [
        BASE_DIR.parent / "frontend" / "public" / "downloads" / "onion-iq.apk",
        BASE_DIR.parent / "frontend_mobile" / "build" / "app" / "outputs" / "flutter-apk" / "app-release.apk",
        BASE_DIR.parent / "frontend_mobile" / "build" / "app" / "outputs" / "flutter-apk" / "app-debug.apk",
    ]
    for apk_path in apk_candidates:
        if apk_path.exists():
            return FileResponse(
                path=str(apk_path),
                filename="onion-iq.apk",
                media_type="application/vnd.android.package-archive"
            )
    raise HTTPException(status_code=404, detail="APK file not found. Please build the mobile app first.")

