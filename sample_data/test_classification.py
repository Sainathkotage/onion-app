import urllib.request
import json
from pathlib import Path

def test_stage3():
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

    # 2. Detect onions
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
        print(f"2. Detection Succeeded! Total Onions: {detect_res['total_onions']}")

    # 3. Classify onion defects
    classify_url = 'http://127.0.0.1:8000/api/analyze/classify'
    classify_payload = json.dumps({
        "upload_id": upload_res["upload_id"],
        "onions": detect_res["onions"]
    }).encode('utf-8')

    req_classify = urllib.request.Request(
        classify_url,
        data=classify_payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with urllib.request.urlopen(req_classify) as response:
        classify_res = json.loads(response.read().decode('utf-8'))
        print(f"3. Defect Classification Succeeded! Engine: {classify_res['classifier_used']}")
        print("--- CLASSIFICATION RESULTS ---")
        for item in classify_res['classifications']:
            print(f"   - {item['label']}: Class = {item['class_label']} (Conf: {item['confidence']*100:.0f}%), Reason = {item['defect_reason']}")

if __name__ == '__main__':
    test_stage3()
