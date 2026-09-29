import cv2
import numpy as np
from pathlib import Path
import sys

# Add backend directory to sys.path
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.services.detector.cv_detector import CVOnionDetector

def create_two_onions_image():
    # Create realistic test canvas with table texture (1920x1080)
    canvas = np.full((1080, 1920, 3), (180, 190, 200), dtype=np.uint8)
    
    # Add subtle background noise/texture
    noise = np.random.randint(-15, 15, canvas.shape, dtype=np.int16)
    canvas = np.clip(canvas.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Onion 1: Golden-brown reddish onion on left side
    cv2.ellipse(canvas, (600, 540), (160, 180), 10, 0, 360, (40, 80, 170), -1)
    # Inner gradient / reflection
    cv2.ellipse(canvas, (570, 500), (90, 100), 10, 0, 360, (70, 120, 210), -1)
    # Root tip / neck
    cv2.line(canvas, (600, 360), (605, 310), (30, 60, 120), 8)

    # Onion 2: Golden-brown onion on right side
    cv2.ellipse(canvas, (1350, 560), (170, 170), -5, 0, 360, (35, 75, 165), -1)
    # Inner gradient / reflection
    cv2.ellipse(canvas, (1320, 520), (100, 95), -5, 0, 360, (65, 115, 205), -1)
    # Root tip / neck
    cv2.line(canvas, (1350, 390), (1345, 330), (25, 55, 110), 8)

    test_path = Path(__file__).resolve().parent / "test_2_onions.jpg"
    cv2.imwrite(str(test_path), canvas)
    return str(test_path)

if __name__ == "__main__":
    img_path = create_two_onions_image()
    print(f"Generated test image with 2 onions: {img_path}")

    detector = CVOnionDetector()
    result = detector.detect(img_path, "test_verification_upload")

    print("\n--- DETECTION RESULTS ---")
    print(f"Detector Used: {result['detector_used']}")
    print(f"Total Candidates (raw): {result['debug_metrics']['total_candidates']}")
    print(f"Rejected by Area: {result['debug_metrics']['rejected_by_area']}")
    print(f"Rejected by Shape: {result['debug_metrics']['rejected_by_shape']}")
    print(f"Final Deduplicated Onions: {result['total_onions']}")

    for o in result['onions']:
        print(f" - {o['label']}: bbox={o['bbox']}, confidence={o['confidence']}, area={o['area']}")

    assert result['total_onions'] == 2, f"FAILED: Expected 2 onions, but got {result['total_onions']}"
    print("\nSUCCESS: Exactly 2 onions detected with 0 overcounting!")
