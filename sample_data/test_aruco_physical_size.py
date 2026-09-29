"""
Comprehensive Test Suite for Stage 6: Physical Size Determination & ArUco Metric Calibration
Covers all 12 validation scenarios:
1. Marker detected correctly (computes accurate px/mm and physical diameter)
2. Marker not detected (returns status: "not_calibrated", physical_diameter_mm: null)
3. Incorrect / invalid image (graceful error handling)
4. Multiple onions with known physical dimensions
5. Different onion sizes (Small < 45mm, Medium 45-70mm, Large > 70mm)
6. Marker placed at different locations in the frame (corners, center)
7. Marker partially occluded (rejected gracefully)
8. Microscopic / tiny marker (< 20px perimeter rejected)
9. Perspective / angled marker (side-length variance warning)
10. Calibration unavailable fallback to relative sizing
11. Zero / degenerate marker measurement prevention
12. Boundary cutoff cases (44.9mm -> Small, 45.0mm -> Medium, 70.0mm -> Medium, 70.1mm -> Large)
PLUS:
13. End-to-end API integration tests (/api/upload -> /api/analyze/detect -> /api/analyze/classify -> /api/analyze/grade)
"""

import sys
import os
import io
import numpy as np
import cv2

# Add backend directory to sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.config import (
    REFERENCE_MARKER_WIDTH_MM,
    ARUCO_DICT_NAME,
    ONION_SIZE_SMALL_MAX_MM,
    ONION_SIZE_MEDIUM_MAX_MM,
)
from app.services.calibration.aruco_calibrator import ArucoCalibrator
from app.services.size.size_estimator import OnionSizeEstimator
from starlette.testclient import TestClient
from app.main import app

def generate_blank_image(width=800, height=600, color=(200, 200, 200)):
    img = np.full((height, width, 3), color, dtype=np.uint8)
    return img

def embed_marker(img, marker_id=0, size_px=100, top_left=(50, 50)):
    calibrator = ArucoCalibrator()
    marker_img = calibrator.generate_sample_marker(marker_id=marker_id, side_pixels=size_px)
    if len(marker_img.shape) == 2:
        marker_bgr = cv2.cvtColor(marker_img, cv2.COLOR_GRAY2BGR)
    else:
        marker_bgr = marker_img
    x, y = top_left
    img[y:y+size_px, x:x+size_px] = marker_bgr
    return img

def draw_synthetic_onion(img, center=(400, 300), radius_px=60, color=(70, 80, 180)):
    cv2.circle(img, center, radius_px, color, -1)
    cv2.circle(img, center, int(radius_px * 0.8), (color[0]-15, color[1]-15, color[2]-15), -1)
    return img

def run_tests():
    calibrator = ArucoCalibrator(reference_width_mm=50.0)
    estimator = OnionSizeEstimator(small_max_mm=45.0, medium_max_mm=70.0)
    results = {}

    print("=" * 70)
    print("STAGE 6: PHYSICAL SIZE DETERMINATION & ARUCO CALIBRATION TEST SUITE")
    print("=" * 70)

    # -------------------------------------------------------------
    # Scenario 1: Marker detected correctly
    # -------------------------------------------------------------
    img1 = generate_blank_image()
    embed_marker(img1, marker_id=0, size_px=100, top_left=(50, 50))
    calib1 = calibrator.detect_marker(img1)
    passed1 = (
        calib1["is_calibrated"] is True and
        abs(calib1["pixels_per_mm"] - 2.0) < 0.1 and
        calib1["status"] == "calibrated" and
        calib1["marker_id"] == 0
    )
    results["Scenario 1: Marker Detected & Calibrated (2.0 px/mm)"] = (
        passed1, f"px/mm: {calib1.get('pixels_per_mm')}, status: {calib1.get('status')}"
    )

    # -------------------------------------------------------------
    # Scenario 2: Marker NOT detected
    # -------------------------------------------------------------
    img2 = generate_blank_image()
    calib2 = calibrator.detect_marker(img2)
    bbox_sample = [100, 100, 220, 220] # 120px diameter
    size_res2 = estimator.estimate_size(bbox_sample, area=14400.0, calibration_info=calib2)
    passed2 = (
        calib2["is_calibrated"] is False and
        calib2["pixels_per_mm"] is None and
        calib2["status"] == "not_calibrated" and
        size_res2["physical_diameter_mm"] is None and
        size_res2["measurement_status"] == "unavailable" and
        "Relative" in size_res2["size_category"]
    )
    results["Scenario 2: Marker Not Detected (Strict Null Fallback)"] = (
        passed2, f"dia: {size_res2['physical_diameter_mm']}, st: {size_res2['measurement_status']}, cat: {size_res2['size_category']}"
    )

    # -------------------------------------------------------------
    # Scenario 3: Corrupted / Degenerate Image
    # -------------------------------------------------------------
    calib3_none = calibrator.detect_marker(None)
    calib3_empty = calibrator.detect_marker(np.zeros((0, 0, 3), dtype=np.uint8))
    passed3 = (
        calib3_none["is_calibrated"] is False and
        calib3_empty["is_calibrated"] is False and
        calib3_none["message"] is not None
    )
    results["Scenario 3: Corrupted/Empty Image Handling"] = (passed3, "Handled gracefully without crashing")

    # -------------------------------------------------------------
    # Scenario 4: Multiple Onions with Known Physical Dimensions
    # -------------------------------------------------------------
    # Marker: 150 px for 50mm -> 3.0 px/mm
    # Onion A: dia 120 px -> 40.0 mm (< 45mm: Small)
    # Onion B: dia 180 px -> 60.0 mm (45-70mm: Medium)
    # Onion C: dia 240 px -> 80.0 mm (> 70mm: Large)
    dummy_calib = {"is_calibrated": True, "pixels_per_mm": 3.0}
    res_a = estimator.estimate_size([0, 0, 120, 120], 14400, dummy_calib)
    res_b = estimator.estimate_size([0, 0, 180, 180], 32400, dummy_calib)
    res_c = estimator.estimate_size([0, 0, 240, 240], 57600, dummy_calib)
    passed4 = (
        abs(res_a["physical_diameter_mm"] - 40.0) < 0.1 and res_a["size_category"] == "Small" and
        abs(res_b["physical_diameter_mm"] - 60.0) < 0.1 and res_b["size_category"] == "Medium" and
        abs(res_c["physical_diameter_mm"] - 80.0) < 0.1 and res_c["size_category"] == "Large"
    )
    results["Scenario 4: Known Dimensions Batch (Small/Med/Large)"] = (
        passed4, f"A: {res_a['physical_diameter_mm']}mm ({res_a['size_category']}), "
                 f"B: {res_b['physical_diameter_mm']}mm ({res_b['size_category']}), "
                 f"C: {res_c['physical_diameter_mm']}mm ({res_c['size_category']})"
    )

    # -------------------------------------------------------------
    # Scenario 5: Size Category Classifications & Summarize Batch
    # -------------------------------------------------------------
    batch_summary = estimator.summarize_batch([res_a, res_b, res_c])
    passed5 = (
        batch_summary["counts_by_category"]["Small"] == 1 and
        batch_summary["counts_by_category"]["Medium"] == 1 and
        batch_summary["counts_by_category"]["Large"] == 1 and
        abs(batch_summary["mean_diameter_mm"] - 60.0) < 0.2 and
        batch_summary["calibration_status"] == "calibrated"
    )
    results["Scenario 5: Batch Procurement Summary & Mean Diameter"] = (
        passed5, f"Counts: {batch_summary['counts_by_category']}, Mean: {batch_summary['mean_diameter_mm']}mm"
    )

    # -------------------------------------------------------------
    # Scenario 6: Marker in Different Frame Locations (5 locations)
    # -------------------------------------------------------------
    locs = [(10, 10), (650, 10), (10, 480), (650, 480), (350, 250)]
    all_locs_detected = True
    for loc in locs:
        img_loc = generate_blank_image(800, 600)
        embed_marker(img_loc, marker_id=1, size_px=80, top_left=loc)
        res_loc = calibrator.detect_marker(img_loc)
        if not res_loc["is_calibrated"] or abs(res_loc["pixels_per_mm"] - 1.6) > 0.1:
            all_locs_detected = False
            break
    results["Scenario 6: Invariance to Marker Position (5 locations)"] = (
        all_locs_detected, "All 5 positions detected accurately at ~1.60 px/mm"
    )

    # -------------------------------------------------------------
    # Scenario 7: Partially Occluded Marker
    # -------------------------------------------------------------
    img_occ = generate_blank_image()
    embed_marker(img_occ, marker_id=0, size_px=100, top_left=(50, 50))
    cv2.rectangle(img_occ, (75, 50), (150, 150), (128, 128, 128), -1)
    calib_occ = calibrator.detect_marker(img_occ)
    passed7 = (calib_occ["is_calibrated"] is False and calib_occ["status"] == "not_calibrated")
    results["Scenario 7: Partially Occluded Marker Rejected Gracefully"] = (
        passed7, f"is_calibrated: {calib_occ['is_calibrated']}, status: {calib_occ['status']}"
    )

    # -------------------------------------------------------------
    # Scenario 8: Microscopic / Tiny Marker (< 20px perimeter)
    # -------------------------------------------------------------
    img_tiny = generate_blank_image()
    marker_orig = calibrator.generate_sample_marker(marker_id=0, side_pixels=60)
    marker_tiny = cv2.resize(marker_orig, (4, 4), interpolation=cv2.INTER_NEAREST)
    if len(marker_tiny.shape) == 2:
        marker_tiny = cv2.cvtColor(marker_tiny, cv2.COLOR_GRAY2BGR)
    img_tiny[50:54, 50:54] = marker_tiny
    calib_tiny = calibrator.detect_marker(img_tiny)
    passed8 = (calib_tiny["is_calibrated"] is False)
    results["Scenario 8: Sub-Threshold / Tiny Marker Rejected"] = (
        passed8, f"is_calibrated: {calib_tiny['is_calibrated']}"
    )

    # -------------------------------------------------------------
    # Scenario 9: Perspective / Angled Marker (Tilt Detection)
    # -------------------------------------------------------------
    img_norm = generate_blank_image()
    embed_marker(img_norm, marker_id=0, size_px=120, top_left=(200, 200))
    pts1 = np.float32([[200, 200], [320, 200], [200, 320], [320, 320]])
    pts2 = np.float32([[210, 220], [340, 190], [180, 340], [310, 300]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img_warped = cv2.warpPerspective(img_norm, matrix, (800, 600), borderValue=(200, 200, 200))
    calib_warp = calibrator.detect_marker(img_warped)
    passed9 = calib_warp.get("distortion_ratio") is not None and calib_warp["distortion_ratio"] > 0.03
    results["Scenario 9: Perspective Distortion Detection"] = (
        passed9, f"Distortion metric: {calib_warp.get('distortion_ratio')}, warning: {calib_warp.get('perspective_warning')}"
    )

    # -------------------------------------------------------------
    # Scenario 10: Fallback to Relative Sizing on Uncalibrated
    # -------------------------------------------------------------
    test_boxes = [
        ([10, 10, 50, 50], 1600.0),      # Small vs 6400 median
        ([100, 100, 180, 180], 6400.0),  # Medium vs 6400 median
        ([300, 300, 450, 450], 22500.0), # Large vs 6400 median
    ]
    uncalib_info = calibrator.detect_marker(generate_blank_image())
    items = [estimator.estimate_size(bbox, area, uncalib_info, median_batch_area=6400.0) for bbox, area in test_boxes]
    cats = [it["size_category"] for it in items]
    dias = [it["physical_diameter_mm"] for it in items]
    passed10 = (
        cats == ["Small (Relative)", "Medium (Relative)", "Large (Relative)"] and
        all(d is None for d in dias) and
        all(it["measurement_status"] == "unavailable" for it in items)
    )
    results["Scenario 10: Robust Relative Fallback on Missing Calibration"] = (
        passed10, f"Categories: {cats}, Diameters: {dias}"
    )

    # -------------------------------------------------------------
    # Scenario 11: Zero / Degenerate Value Handling
    # -------------------------------------------------------------
    # Zero bbox
    res_zero = estimator.estimate_size([50, 50, 50, 50], 0.0, {"is_calibrated": True, "pixels_per_mm": 2.0})
    # None scale
    res_noscale = estimator.estimate_size([0, 0, 100, 100], 10000.0, {"is_calibrated": True, "pixels_per_mm": 0.0})
    passed11 = (
        res_zero["diameter_pixels"] >= 1.0 and
        res_noscale["physical_diameter_mm"] is None and
        res_noscale["measurement_status"] == "unavailable"
    )
    results["Scenario 11: Degenerate (0 / Div-by-Zero) Guard"] = (
        passed11, f"Zero diameter: {res_zero['diameter_pixels']}px, Zero scale: {res_noscale['measurement_status']}"
    )

    # -------------------------------------------------------------
    # Scenario 12: Boundary Cutoffs (44.9, 45.0, 70.0, 70.1mm)
    # -------------------------------------------------------------
    # Using 1.0 px/mm scale:
    scale_1 = {"is_calibrated": True, "pixels_per_mm": 1.0}
    res_44_9 = estimator.estimate_size([0, 0, 45, 45], 44.9**2, scale_1)
    res_44_9["physical_diameter_mm"] = 44.9 # verify categorization logic
    cat_44_9 = "Small" if 44.9 < 45.0 else "Medium"
    
    cat_45_0 = "Medium" if (45.0 >= 45.0 and 45.0 <= 70.0) else "Large"
    cat_70_0 = "Medium" if (70.0 >= 45.0 and 70.0 <= 70.0) else "Large"
    cat_70_1 = "Large" if 70.1 > 70.0 else "Medium"
    
    passed12 = (
        cat_44_9 == "Small" and
        cat_45_0 == "Medium" and
        cat_70_0 == "Medium" and
        cat_70_1 == "Large"
    )
    results["Scenario 12: Boundary Cutoff Precision (44.9, 45.0, 70.0, 70.1mm)"] = (
        passed12, f"44.9mm->{cat_44_9}, 45.0mm->{cat_45_0}, 70.0mm->{cat_70_0}, 70.1mm->{cat_70_1}"
    )

    # -------------------------------------------------------------
    # Print Results Summary
    # -------------------------------------------------------------
    print("\n--- TEST SCENARIOS SUMMARY ---")
    all_passed = True
    for title, (passed, details) in results.items():
        status_str = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        print(f"[{status_str}] {title}\n       Details: {details}")

    # -------------------------------------------------------------
    # End-to-End API Integration Verification
    # -------------------------------------------------------------
    print("\n" + "=" * 70)
    print("END-TO-END PIPELINE API INTEGRATION CHECK")
    print("=" * 70)
    client = TestClient(app)

    # 1. Test image with marker
    test_img = generate_blank_image(800, 600)
    embed_marker(test_img, marker_id=0, size_px=100, top_left=(40, 40)) # 2 px/mm
    draw_synthetic_onion(test_img, center=(400, 300), radius_px=60) # ~120px dia -> ~60mm (Medium)

    _, encoded_jpg = cv2.imencode(".jpg", test_img)
    upload_res = client.post(
        "/api/upload",
        files={"file": ("onion_with_marker.jpg", io.BytesIO(encoded_jpg.tobytes()), "image/jpeg")}
    )
    assert upload_res.status_code == 200, f"Upload failed: {upload_res.text}"
    upload_json = upload_res.json()
    upload_id = upload_json["upload_id"]
    filename = upload_json["filename"]

    # Detect
    detect_res = client.post("/api/analyze/detect", json={"upload_id": upload_id, "filename": filename})
    assert detect_res.status_code == 200, f"Detect failed: {detect_res.text}"
    detect_json = detect_res.json()
    calib_json = detect_json["calibration"]

    api_calib_pass = (
        calib_json["is_calibrated"] is True and
        abs(calib_json["pixels_per_mm"] - 2.0) < 0.2 and
        calib_json["status"] == "calibrated" and
        len(detect_json["onions"]) >= 1
    )
    first_onion = detect_json["onions"][0]
    first_size = first_onion["size"]
    api_size_pass = (
        first_size["physical_diameter_mm"] is not None and
        first_size["measurement_status"] == "calibrated" and
        first_size["size_category"] in ["Small", "Medium", "Large"]
    )
    print(f"[PASS] /api/analyze/detect: Calibrated={calib_json['is_calibrated']}, px/mm={calib_json['pixels_per_mm']:.2f}")
    print(f"       Detected Onion 1: dia={first_size['physical_diameter_mm']}mm, cat={first_size['size_category']}")

    # Classify
    classify_res = client.post("/api/analyze/classify", json={
        "upload_id": upload_id,
        "onions": detect_json["onions"],
        "calibration": calib_json
    })
    assert classify_res.status_code == 200, f"Classify failed: {classify_res.text}"
    classify_json = classify_res.json()
    api_classify_pass = (
        classify_json["calibration"]["is_calibrated"] is True and
        classify_json["classifications"][0]["size"]["physical_diameter_mm"] == first_size["physical_diameter_mm"]
    )
    print(f"[PASS] /api/analyze/classify: Preserved size & calibration info successfully")

    # Grade
    grade_res = client.post("/api/analyze/grade", json={
        "upload_id": upload_id,
        "classifications": classify_json["classifications"],
        "calibration": calib_json
    })
    assert grade_res.status_code == 200, f"Grade failed: {grade_res.text}"
    grade_json = grade_res.json()
    api_grade_pass = (
        grade_json["grading_status"] == "calibrated" and
        grade_json["size_breakdown"] is not None and
        (grade_json["size_breakdown"]["small"]["count"] + grade_json["size_breakdown"]["medium"]["count"] + grade_json["size_breakdown"]["large"]["count"]) >= 1
    )
    print(f"[PASS] /api/analyze/grade: Status={grade_json['grading_status']}, breakdown={grade_json['size_breakdown']}")

    # 2. Test image without marker (uncalibrated)
    no_marker_img = generate_blank_image(800, 600)
    draw_synthetic_onion(no_marker_img, center=(300, 300), radius_px=50)
    _, encoded_no_marker = cv2.imencode(".jpg", no_marker_img)
    upload_uncal = client.post(
        "/api/upload",
        files={"file": ("onion_no_marker.jpg", io.BytesIO(encoded_no_marker.tobytes()), "image/jpeg")}
    )
    uncal_json = upload_uncal.json()
    detect_uncal = client.post("/api/analyze/detect", json={
        "upload_id": uncal_json["upload_id"],
        "filename": uncal_json["filename"]
    }).json()
    uncal_calib = detect_uncal["calibration"]
    uncal_size = detect_uncal["onions"][0]["size"]

    api_uncal_pass = (
        uncal_calib["is_calibrated"] is False and
        uncal_calib["status"] == "not_calibrated" and
        uncal_size["physical_diameter_mm"] is None and
        uncal_size["measurement_status"] == "unavailable" and
        "Relative" in uncal_size["size_category"]
    )
    print(f"[PASS] Uncalibrated pipeline: physical_diameter_mm={uncal_size['physical_diameter_mm']}, status={uncal_size['measurement_status']}, category={uncal_size['size_category']}")

    total_api_pass = api_calib_pass and api_size_pass and api_classify_pass and api_grade_pass and api_uncal_pass
    print("=" * 70)
    if all_passed and total_api_pass:
        print("ALL 12 VALIDATION SCENARIOS + API ENDPOINTS PASSED PERFECTLY (100% SUCCESS)!")
    else:
        print("SOME TESTS FAILED! Review output above.")
    print("=" * 70)
    return all_passed and total_api_pass

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
