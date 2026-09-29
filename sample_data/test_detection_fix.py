import urllib.request
import json
import cv2
import numpy as np
from pathlib import Path

def test_detection_fix():
    print("==================================================")
    print("  ONION DETECTION PIPELINE ACCEPTEST & DEBUG RUN  ")
    print("==================================================")

    # 1. Restart Backend Server Verification via Health Check
    health_url = 'http://127.0.0.1:8000/api/health'
    try:
        res = urllib.request.urlopen(health_url)
        print("Backend API is Online:", json.loads(res.read().decode()))
    except Exception as e:
        print("Backend API offline:", e)
        return

    # 2. Upload & Detect sample_onions_tray.jpg
    upload_url = 'http://127.0.0.1:8000/api/upload'
    filepath = Path('sample_onions_tray.jpg')
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    
    with open(filepath, 'rb') as f:
        file_bytes = f.read()
        
    header = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="file"; filename="{filepath.name}"\r\n'
        f'Content-Type: image/jpeg\r\n\r\n'
    ).encode('utf-8')
    footer = f'\r\n--{boundary}--\r\n'.encode('utf-8')
    body = header + file_bytes + footer
    
    req = urllib.request.Request(
        upload_url,
        data=body,
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'},
        method='POST'
    )
    
    with urllib.request.urlopen(req) as response:
        upload_res = json.loads(response.read().decode('utf-8'))
        upload_id = upload_res["upload_id"]
        print(f"\n1. Image Uploaded: {upload_id} (Size: {upload_res['width']}x{upload_res['height']} px)")

    # Execute Detection API
    detect_url = 'http://127.0.0.1:8000/api/analyze/detect'
    detect_payload = json.dumps({
        "upload_id": upload_id,
        "filename": upload_res["filename"]
    }).encode('utf-8')
    
    req_detect = urllib.request.Request(
        detect_url,
        data=detect_payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    with urllib.request.urlopen(req_detect) as response:
        detect_res = json.loads(response.read().decode('utf-8'))
        print(f"\n2. Detection Response:")
        print(f"   Detector Engine Used: {detect_res['detector_used']}")
        print(f"   Total Onions Detected: {detect_res['total_onions']}")
        
        onions = detect_res["onions"]
        if onions:
            confidences = [o["confidence"] for o in onions]
            avg_conf = sum(confidences) / len(confidences)
            print(f"   Average Confidence: {avg_conf * 100:.1f}%")
        
        print("\n--- INDIVIDUAL ONION DETECTIONS ---")
        for o in onions:
            print(f"   - {o['label']}: BBox=[{o['bbox'][0]}, {o['bbox'][1]}, {o['bbox'][2]}, {o['bbox'][3]}], Area={int(o['area'])} px^2, Conf={o['confidence']*100:.0f}%")

    # Verify Debug Files Saved in backend/debug/
    debug_dir = Path(__file__).parent.parent / "backend" / "debug"
    debug_files = list(debug_dir.glob(f"{upload_id}_*"))
    print(f"\n3. Visual Debug Files Generated in backend/debug/: {len(debug_files)} files")
    for df in debug_files:
        print(f"   - {df.name}")

if __name__ == '__main__':
    test_detection_fix()
