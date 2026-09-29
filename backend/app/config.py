import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from backend/.env or root .env
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

DEBUG_DIR = BASE_DIR / "debug"
DEBUG_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE_MB = 20
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

# Google Gemini Vision Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
SUPPRESS_OTHER_MODELS = os.getenv("SUPPRESS_OTHER_MODELS", "true").lower() == "true"

# Legacy / Suppressed Models (Roboflow)
ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY", "")
ROBOFLOW_MODEL_ID = os.getenv("ROBOFLOW_MODEL_ID", "onion-disease/3")
ROBOFLOW_API_URL = os.getenv("ROBOFLOW_API_URL", "https://serverless.roboflow.com")
ROBOFLOW_CONFIDENCE = float(os.getenv("ROBOFLOW_CONFIDENCE", "0.25"))

# Detector Configuration
DETECTOR_MODE = os.getenv("DETECTOR_MODE", "gemini").lower()
ONION_DETECTOR_TYPE = os.getenv("ONION_DETECTOR_TYPE", "gemini").lower()
ONION_CLASSIFIER_TYPE = os.getenv("ONION_CLASSIFIER_TYPE", "gemini").lower()
ONION_DETECTOR_MODEL = os.getenv("ONION_DETECTOR_MODEL", str(BASE_DIR / "models" / "onion_detector.pt"))

# Post-processing & Filtering Thresholds (Permissive for dark/purple/dirty onions & shadows)
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.20"))
IOU_THRESHOLD = float(os.getenv("IOU_THRESHOLD", "0.35"))
MIN_ONION_AREA_PIXELS = int(os.getenv("MIN_ONION_AREA_PIXELS", "250"))
MAX_ONION_AREA_RATIO = float(os.getenv("MAX_ONION_AREA_RATIO", "0.55"))
DEBUG_SAVE_PIPELINE = os.getenv("DEBUG_SAVE_PIPELINE", "true").lower() == "true"

# Reference Scale & Physical Sizing Configuration (ArUco Fiducial Marker)
REFERENCE_MARKER_WIDTH_MM = float(os.getenv("REFERENCE_MARKER_WIDTH_MM", "50.0"))
ARUCO_DICT_NAME = os.getenv("ARUCO_DICT_NAME", "DICT_4X4_50")

# Physical Size Category Thresholds (Standard Agricultural Procurement Baseline)
ONION_SIZE_SMALL_MAX_MM = float(os.getenv("ONION_SIZE_SMALL_MAX_MM", "45.0"))
ONION_SIZE_MEDIUM_MAX_MM = float(os.getenv("ONION_SIZE_MEDIUM_MAX_MM", "70.0"))

