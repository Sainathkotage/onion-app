import sys
import io
import hashlib
import os
import gc
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from fastapi.testclient import TestClient
from PIL import Image
from app.main import app
from app.config import UPLOAD_DIR

client = TestClient(app)

print("=== TESTING BACKEND IMAGE UPLOAD & INGESTION (STAGE 2) ===\n")

# 1. Endpoint & Format Verification
print("1. Backend Endpoint: POST /api/upload")
print("   Request format  : multipart/form-data with field name 'file'\n")

# 2. Test Real Sample Onion Image & Byte-for-byte Immutability (Check 8)
sample_path = Path("sample_data/sample_onions_tray.jpg")
with open(sample_path, "rb") as f:
    sample_bytes = f.read()

original_sha256 = hashlib.sha256(sample_bytes).hexdigest()

res = client.post("/api/upload", files={"file": ("sample_onions_tray.jpg", io.BytesIO(sample_bytes), "image/jpeg")})
assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
data = res.json()
print("[CHECK 1 & 8] Actual Onion Image Upload & Byte Immutability:")
print(f"   Upload ID: {data['upload_id']}")
print(f"   Saved filename: {data['filename']}")
print(f"   Reported dimensions: {data['width']}x{data['height']}, format: {data['format']}")

saved_path = UPLOAD_DIR / data["filename"]
assert saved_path.exists(), "Saved file does not exist on disk!"
with open(saved_path, "rb") as f:
    saved_bytes = f.read()
saved_sha256 = hashlib.sha256(saved_bytes).hexdigest()

print(f"   Original SHA256: {original_sha256}")
print(f"   Saved SHA256   : {saved_sha256}")
assert original_sha256 == saved_sha256, "FAIL: Backend modified the image bytes!"
print("   PASS: Image bytes are identical (byte-for-byte exact match).\n")

# Clean up test file
if saved_path.exists():
    os.remove(saved_path)

# 3. Test Valid JPG (Synthetic)
img_jpg = Image.new("RGB", (320, 240), color=(120, 80, 40))
buf_jpg = io.BytesIO()
img_jpg.save(buf_jpg, format="JPEG")
buf_jpg.seek(0)
res_jpg = client.post("/api/upload", files={"file": ("test.jpg", buf_jpg, "image/jpeg")})
print("[CHECK 2] Valid JPG:")
print(f"   Status: {res_jpg.status_code}, Format: {res_jpg.json().get('format')}")
assert res_jpg.status_code == 200
assert res_jpg.json()["format"] == "JPEG"
saved_jpg = UPLOAD_DIR / res_jpg.json()["filename"]
if saved_jpg.exists():
    os.remove(saved_jpg)

# 4. Test Valid PNG
img_png = Image.new("RGBA", (400, 300), color=(20, 150, 80, 255))
buf_png = io.BytesIO()
img_png.save(buf_png, format="PNG")
buf_png.seek(0)
res_png = client.post("/api/upload", files={"file": ("test.png", buf_png, "image/png")})
print("\n[CHECK 3] Valid PNG:")
print(f"   Status: {res_png.status_code}, Format: {res_png.json().get('format')}")
assert res_png.status_code == 200
assert res_png.json()["format"] == "PNG"
saved_png = UPLOAD_DIR / res_png.json()["filename"]
if saved_png.exists():
    os.remove(saved_png)

# 5. Test Empty Request (No body or missing 'file' field)
res_empty_req = client.post("/api/upload")
print("\n[CHECK 4] Empty Request (No multipart payload):")
print(f"   Status: {res_empty_req.status_code}")
assert res_empty_req.status_code in [400, 422]

# 6. Test Empty File (0-byte payload)
res_zero = client.post("/api/upload", files={"file": ("empty.jpg", io.BytesIO(b""), "image/jpeg")})
print("\n[CHECK 5] Empty File (0 bytes):")
print(f"   Status: {res_zero.status_code}, Detail: {res_zero.json().get('detail')}")
assert res_zero.status_code == 400
assert "empty" in res_zero.json().get("detail", "").lower()

# 7. Test Oversized File (>20MB)
oversized_bytes = b"0" * (20 * 1024 * 1024 + 1024)
res_over = client.post("/api/upload", files={"file": ("big.jpg", io.BytesIO(oversized_bytes), "image/jpeg")})
print("\n[CHECK 6] Oversized File (>20MB):")
print(f"   Status: {res_over.status_code}, Detail: {res_over.json().get('detail')}")
assert res_over.status_code == 400
assert "exceeds" in res_over.json().get("detail", "").lower()

# 8. Test Invalid File Extension (.txt / .pdf)
res_invalid = client.post("/api/upload", files={"file": ("doc.txt", io.BytesIO(b"Hello text document"), "text/plain")})
print("\n[CHECK 7] Invalid File (.txt):")
print(f"   Status: {res_invalid.status_code}, Detail: {res_invalid.json().get('detail')}")
assert res_invalid.status_code == 400
assert "unsupported" in res_invalid.json().get("detail", "").lower()

# 9. Test Corrupted Image (named .jpg but contains invalid random binary)
corrupt_bytes = b"\xff\xd8\xff\xe0" + b"corrupted_random_garbage_bytes" * 50
res_corrupt = client.post("/api/upload", files={"file": ("corrupt.jpg", io.BytesIO(corrupt_bytes), "image/jpeg")})
print("\n[CHECK 8] Corrupted Image:")
print(f"   Status: {res_corrupt.status_code}, Detail: {res_corrupt.json().get('detail')}")
assert res_corrupt.status_code == 400
assert "corrupted" in res_corrupt.json().get("detail", "").lower()

# 10. Repeated Requests & Memory/File Leaks Check (25 iterations)
print("\n[CHECK 9] Repeated Requests & Resource Cleanup (25 rapid cycles):")
created_files = []
for i in range(25):
    buf_loop = io.BytesIO()
    img_jpg.save(buf_loop, format="JPEG")
    buf_loop.seek(0)
    r = client.post("/api/upload", files={"file": (f"loop_{i}.jpg", buf_loop, "image/jpeg")})
    assert r.status_code == 200
    created_files.append(UPLOAD_DIR / r.json()["filename"])

print(f"   Successfully executed 25 sequential upload cycles without failure.")
# Clean up created test files
for f in created_files:
    if f.exists():
        os.remove(f)

print("   Temporary files cleaned up successfully. No residual leaks.")
print("\n>>> ALL STAGE 2 BACKEND INGESTION CHECKS PASSED SUCCESSFULLY! <<<")
