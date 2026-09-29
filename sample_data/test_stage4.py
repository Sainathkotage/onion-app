import urllib.request
import json
from pathlib import Path

def test_stage4():
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
        upload_id = upload_res["upload_id"]
        print("1. Upload Succeeded:", upload_id)

    # 2. Detect onions
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
        print(f"2. Detection Succeeded! Total Onions: {detect_res['total_onions']}")

    # 3. Classify onion defects
    classify_url = 'http://127.0.0.1:8000/api/analyze/classify'
    classify_payload = json.dumps({
        "upload_id": upload_id,
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
        print("3. Classification Succeeded!")

    # 4. Grade Batch
    grade_url = 'http://127.0.0.1:8000/api/analyze/grade'
    grade_payload = json.dumps({
        "upload_id": upload_id,
        "classifications": classify_res["classifications"]
    }).encode('utf-8')

    req_grade = urllib.request.Request(
        grade_url,
        data=grade_payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with urllib.request.urlopen(req_grade) as response:
        grade_res = json.loads(response.read().decode('utf-8'))
        print("--- GRADING SUMMARY ---")
        print(f"   Batch ID: {grade_res['batch_id']}")
        print(f"   Total Onions: {grade_res['total_onions']}")
        print(f"   Grade A: {grade_res['grade_a']['count']} ({grade_res['grade_a']['percentage']}%)")
        print(f"   URS (Rejected): {grade_res['urs']['count']} ({grade_res['urs']['percentage']}%)")
        print(f"   Recommendation: {grade_res['recommendation']}")

    # 5. Generate PDF Quality Report
    pdf_url = 'http://127.0.0.1:8000/api/reports/pdf'
    pdf_payload = json.dumps({
        "upload_id": upload_id,
        "grading": grade_res,
        "classifications": classify_res["classifications"],
        "annotated_image_url": detect_res["annotated_image_url"]
    }).encode('utf-8')

    req_pdf = urllib.request.Request(
        pdf_url,
        data=pdf_payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with urllib.request.urlopen(req_pdf) as response:
        pdf_res = json.loads(response.read().decode('utf-8'))
        print("4. PDF Generation Succeeded!")
        print(f"   PDF Report Access URL: {pdf_res['pdf_report_url']}")

    # 6. Verify downloading generated PDF file
    pdf_file_url = f"http://127.0.0.1:8000{pdf_res['pdf_report_url']}"
    pdf_bytes = urllib.request.urlopen(pdf_file_url).read()
    print(f"5. Downloaded PDF File Verified! Size: {len(pdf_bytes)} bytes")

if __name__ == '__main__':
    test_stage4()
