import urllib.request
import json
from pathlib import Path

def test_stage2():
    # 1. Upload sample image
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
        print("1. Upload Succeeded:", upload_res["upload_id"])

    # 2. Invoke Detection Endpoint
    detect_url = 'http://127.0.0.1:8000/api/analyze/detect'
    detect_payload = json.dumps({
        "upload_id": upload_res["upload_id"],
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
        print(f"2. Detection Succeeded! Total Onions Detected: {detect_res['total_onions']}")
        print(f"   Annotated Image URL: {detect_res['annotated_image_url']}")
        print(f"   Detector Engine: {detect_res['detector_used']}")
        for onion in detect_res['onions']:
            print(f"   - {onion['label']}: BBox={onion['bbox']}, Crop={onion['crop_path']}, Conf={onion['confidence']}")

if __name__ == '__main__':
    test_stage2()
