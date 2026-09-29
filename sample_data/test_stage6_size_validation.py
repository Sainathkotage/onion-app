import sys
import os
import json
from pathlib import Path
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.services.detector.cv_detector import CVOnionDetector
from app.services.classifier.demo_classifier import DemoOnionClassifier
from app.services.feature_extraction import extract_onion_features

print("=" * 80)
print("          STAGE 6: ONION PHYSICAL SIZE ESTIMATION VALIDATION")
print("=" * 80)

classifier = DemoOnionClassifier(undersized_threshold=0.65)
detector = CVOnionDetector()

# =========================================================================
# TEST 1: Boundary Cases Near the 0.65 Threshold
# =========================================================================
print("\n[TEST 1: BOUNDARY SENSITIVITY TESTING NEAR 0.65 THRESHOLD]")
# Test area ratios: 0.63, 0.64, 0.649, 0.650, 0.651, 0.66, 0.70 against median=10,000 px^2
median_ref = 10000.0
boundary_ratios = [0.50, 0.60, 0.64, 0.649, 0.650, 0.651, 0.66, 0.80, 1.00]

print(f"{'Area (px^2)':<12} | {'Median Ref':<12} | {'Ratio':<8} | {'Expected Class':<15} | {'Predicted Class':<15} | {'Match'}")
print("-" * 80)

for ratio in boundary_ratios:
    test_area = median_ref * ratio
    # Construct batch where the median is strictly median_ref
    # Batch: [median_ref, median_ref, test_area]
    batch = [
        {"id": 1, "label": "Ref 1", "bbox": [0, 0, 100, 100], "area": median_ref, "crop_path": ""},
        {"id": 2, "label": "Ref 2", "bbox": [0, 0, 100, 100], "area": median_ref, "crop_path": ""},
        {"id": 3, "label": "Target", "bbox": [0, 0, int(np.sqrt(test_area)), int(np.sqrt(test_area))], "area": test_area, "crop_path": ""}
    ]
    res = classifier.classify_batch(batch, "boundary_eval")
    target_pred = res["classifications"][2]["class_label"]
    expected = "Undersized" if ratio < 0.65 else "Healthy"
    match = "PASS" if target_pred == expected else "FAIL"
    print(f"{int(test_area):<12} | {int(median_ref):<12} | {ratio:<8.3f} | {expected:<15} | {target_pred:<15} | {match}")

# =========================================================================
# TEST 2: Single-Onion Blind Spot (The N=1 Invariant Failure)
# =========================================================================
print("\n[TEST 2: SINGLE-ONION BATCH BLIND SPOT]")
print("Testing single onion of tiny area (e.g. 2,000 px^2 - physical 25mm cocktail onion)...")
single_tiny = [{"id": 1, "label": "Tiny Onion", "bbox": [0, 0, 45, 45], "area": 2000.0, "crop_path": ""}]
res_single = classifier.classify_batch(single_tiny, "eval_single")
print(f"  Input Area: 2000 px^2 (Tiny)")
print(f"  Calculated Median: {2000.0} px^2")
print(f"  Ratio: 2000 / 2000 = 1.00")
print(f"  Result Class: {res_single['classifications'][0]['class_label']} (Expected: Undersized, Actual: {res_single['classifications'][0]['class_label']})")
print("  Vulnerability: Single isolated onions CANNOT be evaluated for size because median == area.")

# =========================================================================
# TEST 3: All-Undersized Batch Failure (Relative Sizing Blind Spot)
# =========================================================================
print("\n[TEST 3: ALL-UNDERSIZED BATCH BLIND SPOT]")
print("Testing batch where ALL onions are physically undersized (e.g. 2000-2500 px^2)...")
all_tiny_batch = [
    {"id": 1, "label": "Tiny 1", "bbox": [0, 0, 45, 45], "area": 2100.0, "crop_path": ""},
    {"id": 2, "label": "Tiny 2", "bbox": [0, 0, 46, 46], "area": 2200.0, "crop_path": ""},
    {"id": 3, "label": "Tiny 3", "bbox": [0, 0, 48, 48], "area": 2300.0, "crop_path": ""},
    {"id": 4, "label": "Tiny 4", "bbox": [0, 0, 50, 50], "area": 2400.0, "crop_path": ""},
]
res_all_tiny = classifier.classify_batch(all_tiny_batch, "eval_all_tiny")
classes_predicted = [c["class_label"] for c in res_all_tiny["classifications"]]
print(f"  Input Areas: [2100, 2200, 2300, 2400] px^2")
print(f"  Batch Median: 2250 px^2")
print(f"  Result Classes: {classes_predicted}")
print("  Vulnerability: In a tray containing only small/cull onions, ZERO are detected as Undersized.")

# =========================================================================
# TEST 4: Camera Distance & Scale Ambiguity (Physical vs Pixel Diameter)
# =========================================================================
print("\n[TEST 4: CAMERA DISTANCE & SCALE AMBIGUITY]")
print("Case A: 60mm Jumbo Onion photographed from 1.5 meters away -> 80px diameter (area = 5,026 px^2)")
print("Case B: 35mm Undersized Onion photographed from 0.3 meters away -> 180px diameter (area = 25,446 px^2)")
print("  Without a physical reference (coin/ruler/ArUco/known tray grid), Case B appears 5x larger than Case A.")
print("  No camera intrinsics (focal length, sensor pitch) or extrinsics (working distance) are captured in the pipeline.")

# =========================================================================
# TEST 5: Perspective Distortion (Tray Tilt & Depth Gradient)
# =========================================================================
print("\n[TEST 5: PERSPECTIVE DISTORTION IMPACT]")
print("At a 45-degree oblique viewing angle on a 40cm tray:")
print("  - Onion at near edge (Z = 50cm): 100px diameter")
print("  - Identical onion at far edge (Z = 80cm): 62.5px diameter (Area ratio = (62.5/100)^2 = 0.39 < 0.65)")
print("  Result: Two identical onions will be graded differently: Near = Healthy, Far = Undersized.")

# =========================================================================
# TEST 6: Resolution Invariance Verification
# =========================================================================
print("\n[TEST 6: IMAGE RESOLUTION SCALING]")
print("Testing if resolution scaling changes the relative size ratio:")
base_areas = [10000.0, 12000.0, 5000.0, 11000.0] # 5000 is < 0.65 of median 10500
scale_factors = [0.5, 1.0, 2.0, 4.0]

for s in scale_factors:
    scaled_batch = [
        {"id": i, "label": f"O_{i}", "bbox": [0,0,10,10], "area": a * (s**2), "crop_path": ""}
        for i, a in enumerate(base_areas)
    ]
    res_scaled = classifier.classify_batch(scaled_batch, f"eval_scale_{s}")
    preds = [c["class_label"] for c in res_scaled["classifications"]]
    print(f"  Scale Factor {s:3.1f}x (Area {s**2:4.1f}x) -> Predictions: {preds}")

print("\n" + "=" * 80)
print("                     VALIDATION RUN COMPLETE")
print("=" * 80)
