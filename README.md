# OnionIQ — Automated Onion Quality Assessment & Grading Prototype

**Problem Statement ID:** 26031  
**Goal:** Rapid prototype web/mobile application for procurement centers to photograph onion batches, detect individual onions, classify defect classes, calculate Grade A vs URS (Unusable / Rejected Supply) percentages, and export digital PDF quality reports.

---

## Architecture Overview

- **Frontend:** Next.js (App Router), React, TypeScript, Tailwind CSS, Lucide Icons.
- **Backend:** Python FastAPI, Uvicorn, Pillow, OpenCV, Pydantic.
- **Sample Data:** `sample_data/sample_onions_tray.jpg` generated for testing without external dataset.

---

## Local Development Instructions

### 1. Backend Setup & Startup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (if not created)
python -m venv venv

# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
# source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run FastAPI backend server (Port 8000)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend API Health Check: `http://localhost:8000/api/health`

---

### 2. Frontend Setup & Startup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not installed)
npm install

# Start Next.js development server (Port 3000)
npm run dev
```

Open application in browser: `http://localhost:3000`

---

## API Endpoints (Stage 1)

- `GET /api/health`: Returns API health status.
- `POST /api/upload`: Uploads image file, validates format/size, and returns image metadata and upload ID.
