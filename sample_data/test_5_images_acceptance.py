import urllib.request
import json
from pathlib import Path

def run_acceptance_test_5_images():
    print("===============================================================")
    print("  ONION DETECTION ACCEPTANCE TEST ON 5 DIVERSE BATCH IMAGES    ")
    print("===============================================================")

    test_images = [
        "test_img1_purple_cardboard.jpg",
        "test_img2_yellow_wood.jpg",
        "test_img3_metal_conveyor.jpg",
        "test_img4_sprouted_red.jpg",
        "test_img5_mixed_tray.jpg",
    ]

    results_summary = []

    for img_name in test_images:
        filepath = Path(__file__).parent / img_name
        if not filepath.exists():
            print(f"Skipping {img_name}: file not found.")
            continue

        # Upload image
        upload_url = 'http://127.0.0.1:8000/api/upload'
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

        # Detect onions
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
            metrics = detect_res.get("debug_metrics", {})
            
            entry = {
                "image": img_name,
                "detected": detect_res["total_onions"],
                "detector_used": detect_res["detector_used"],
                "total_candidates": metrics.get("total_candidates", 0),
                "rejected_by_area": metrics.get("rejected_by_area", 0),
                "rejected_by_shape": metrics.get("rejected_by_shape", 0),
                "rejected_by_confidence": metrics.get("rejected_by_confidence", 0),
            }
            results_summary.append(entry)

            print(f"\nImage: {img_name}")
            print(f"  Dimensions: {upload_res['width']}x{upload_res['height']} px")
            print(f"  Detected Onions: {entry['detected']}")
            print(f"  Engine: {entry['detector_used']}")
            print(f"  Debug Metrics: Total Candidates={entry['total_candidates']}, RejectedArea={entry['rejected_by_area']}, RejectedShape={entry['rejected_by_shape']}, FinalDetections={entry['detected']}")

    print("\n===============================================================")
    print("                    FINAL ACCEPTANCE SUMMARY                   ")
    print("===============================================================")
    for r in results_summary:
        print(f"  {r['image']}  --->  Detected = {r['detected']} onions (Candidates: {r['total_candidates']})")
    print("===============================================================")

if __name__ == '__main__':
    run_acceptance_test_5_images()
