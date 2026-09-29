import sys
import os
import time
import json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.services.detector.detector_factory import OnionDetectorFactory
from app.services.detector.roboflow_detector import RoboflowOnionDetector
from app.services.detector.cv_detector import CVOnionDetector
from app.services.classifier.classifier_factory import OnionClassifierFactory
from app.services.classifier.demo_classifier import DemoOnionClassifier
from app.services.classifier.densenet121_classifier import DenseNet121OnionClassifier
from app.services.classifier.tflite_classifier import TFLiteOnionClassifier

print("=" * 75)
print("       ML INFERENCE STAGE VALIDATION REPORT (ONION QUALITY PIPELINE)")
print("=" * 75)

# -------------------------------------------------------------------------
# Part 1: Model Audit & Configuration Inspection
# -------------------------------------------------------------------------
print("\n[PART 1: MODEL AUDIT & CONFIGURATION]")

# Detector check
roboflow_detector = RoboflowOnionDetector()
cv_detector = CVOnionDetector()

print("1. Detection Models:")
print(f"   - Roboflow Cloud Detector: Model ID='{roboflow_detector.model_id}', API='{roboflow_detector.api_url}'")
print(f"     Client Configured: {roboflow_detector.client is not None}")
print(f"     Confidence Threshold: {roboflow_detector.conf_threshold}")
print(f"   - OpenCV Content Detector: Active (Hybrid Morphological + HSV)")

# Classifier check
print("2. Classification Models:")
tflite_classifier = TFLiteOnionClassifier()
densenet_classifier = DenseNet121OnionClassifier()
demo_classifier = DemoOnionClassifier()

print(f"   - TFLite Model File: '{tflite_classifier.model_path}' (Exists: {os.path.exists(tflite_classifier.model_path)})")
print(f"     TFLite Runtime Available: {tflite_classifier.model_loaded}")
print(f"   - DenseNet-121 Model Path: '{densenet_classifier.model_path}' (Exists: {os.path.exists(densenet_classifier.model_path)})")
print(f"     PyTorch Device: CPU")
print(f"   - CV Feature Classifier: Active Fallback Engine")

# -------------------------------------------------------------------------
# Part 2: Model Execution & Latency Benchmarking
# -------------------------------------------------------------------------
print("\n[PART 2: MODEL EXECUTION VALIDATION]")

# Test Roboflow execution
rf_image = "sample_data/test_img1_purple_cardboard.jpg"
if os.path.exists(rf_image) and roboflow_detector.client:
    t0 = time.perf_counter()
    rf_res = roboflow_detector.infer_raw(rf_image)
    rf_latency_ms = (time.perf_counter() - t0) * 1000
    rf_preds = rf_res.get("predictions", [])
    print(f"  Roboflow Serverless Inference Latency: {rf_latency_ms:.2f} ms")
    print(f"  Roboflow Predictions Count: {len(rf_preds)}")
    if rf_preds:
        p = rf_preds[0]
        print(f"  Sample Prediction: Class='{p.get('class')}', Conf={p.get('confidence'):.4f}, Box=({p.get('x')}, {p.get('y')}, {p.get('width')}, {p.get('height')})")

# Test CV detector execution
t0 = time.perf_counter()
cv_res = cv_detector.detect("sample_data/sample_onions_tray.jpg", "test_stage4_eval")
cv_latency_ms = (time.perf_counter() - t0) * 1000
print(f"  OpenCV Detector Latency: {cv_latency_ms:.2f} ms | Detected Onions: {cv_res.get('total_onions')}")

# Test Classifier execution
t0 = time.perf_counter()
classifier_res = demo_classifier.classify_batch(cv_res["onions"], "test_stage4_eval")
cls_latency_ms = (time.perf_counter() - t0) * 1000
print(f"  Classifier Latency: {cls_latency_ms:.2f} ms for {len(cv_res['onions'])} crops ({cls_latency_ms/max(1, len(cv_res['onions'])):.2f} ms/crop)")

# -------------------------------------------------------------------------
# Part 3: Model Accuracy & Scenario Robustness Testing (7 Required Scenarios)
# -------------------------------------------------------------------------
print("\n[PART 3: 7 SCENARIO ACCURACY VALIDATION]")

scenarios = [
    ("1. Good / Healthy Onions", "sample_data/test_img2_yellow_wood.jpg"),
    ("2. Defective / Sprouted Onion", "sample_data/test_img4_sprouted_red.jpg"),
    ("3. Multiple Onions Tray", "sample_data/sample_onions_tray.jpg"),
    ("4. Purple Background / Lighting", "sample_data/test_img1_purple_cardboard.jpg"),
    ("5. Conveyor Metal Background", "sample_data/test_img3_metal_conveyor.jpg"),
]

for title, path in scenarios:
    if os.path.exists(path):
        det = cv_detector.detect(path, f"eval_{Path(path).stem}")
        cls = demo_classifier.classify_batch(det["onions"], f"eval_{Path(path).stem}")
        classes_found = [c["class_label"] for c in cls["classifications"]]
        confs = [c["confidence"] for c in cls["classifications"]]
        avg_conf = np.mean(confs) if confs else 0.0
        print(f"\n  Scenario {title} ({path}):")
        print(f"    - Onions Detected : {det['total_onions']}")
        print(f"    - Defect Breakdown: {classes_found}")
        print(f"    - Mean Confidence : {avg_conf:.2f}")

# Scenario 6: No Onions (Empty canvas)
empty_canvas = np.full((600, 800, 3), (200, 200, 200), dtype=np.uint8)
empty_path = "sample_data/eval_no_onions.jpg"
cv2.imwrite(empty_path, empty_canvas)
det_empty = cv_detector.detect(empty_path, "eval_empty")
print(f"\n  Scenario 6. Images with No Onions (Blank Canvas):")
print(f"    - Onions Detected: {det_empty['total_onions']} (Expected: 0)")
if os.path.exists(empty_path):
    os.remove(empty_path)

# Scenario 7: Unrelated Objects (Random non-onion objects / shapes)
unrelated = np.zeros((600, 800, 3), dtype=np.uint8)
cv2.rectangle(unrelated, (100, 100), (300, 400), (255, 0, 0), -1)  # Blue rectangle
cv2.rectangle(unrelated, (450, 200), (700, 500), (0, 255, 255), -1) # Yellow rectangle
unrelated_path = "sample_data/eval_unrelated.jpg"
cv2.imwrite(unrelated_path, unrelated)
det_unrelated = cv_detector.detect(unrelated_path, "eval_unrelated")
print(f"\n  Scenario 7. Images with Unrelated Objects (Blue & Yellow Boxes):")
print(f"    - Onions Detected: {det_unrelated['total_onions']} (Expected: 0)")
if os.path.exists(unrelated_path):
    os.remove(unrelated_path)

print("\n" + "=" * 75)
print("                   VALIDATION SUMMARY")
print("=" * 75)
