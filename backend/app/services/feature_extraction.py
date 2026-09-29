import cv2
import numpy as np
from pathlib import Path

def extract_onion_features(crop_img: np.ndarray, area: float, median_area: float) -> dict:
    """
    Extracts computer vision color, texture, shape, and relative size features from an onion crop image.
    """
    h, w = crop_img.shape[:2]
    total_pixels = max(1, h * w)

    # 1. Relative Size Check
    # Configurable threshold: < 0.65 of median batch area -> Undersized
    size_ratio = area / median_area if median_area > 0 else 1.0
    is_undersized = size_ratio < 0.65

    # Blur crop to reduce noise
    blurred = cv2.GaussianBlur(crop_img, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

    # 2. Green Sprout Feature Detection (HSV hue range 35-85)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    green_pixel_count = cv2.countNonZero(green_mask)
    green_ratio = green_pixel_count / total_pixels
    is_sprouted = green_ratio > 0.005  # >0.5% green pixels indicates sprout growth

    # 3. Dark Rot / Soft Rot Feature Detection
    # Very dark patches (brightness V < 55 and low saturation or dark brown/black rot)
    lower_dark = np.array([0, 0, 0])
    upper_dark = np.array([180, 255, 55])
    dark_mask = cv2.inRange(hsv, lower_dark, upper_dark)
    dark_pixel_count = cv2.countNonZero(dark_mask)
    dark_ratio = dark_pixel_count / total_pixels
    is_rotten = dark_ratio > 0.025  # >2.5% dark rot region

    # 4. Mechanical Damage / Cut / Crack Feature Detection
    # Detects surface cuts, dark fissure cracks, and sharp gradient line density
    edges = cv2.Canny(gray, 50, 150)
    edge_density = cv2.countNonZero(edges) / total_pixels
    
    _, mask = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)
    inner_mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)), iterations=1)
    dark_cuts = cv2.bitwise_and(cv2.inRange(gray, 20, 90), inner_mask)
    cut_ratio = cv2.countNonZero(dark_cuts) / max(1, cv2.countNonZero(inner_mask))
    
    is_damaged = (0.004 < cut_ratio <= 0.035) or edge_density > 0.06

    return {
        "size_ratio": size_ratio,
        "is_undersized": is_undersized,
        "green_ratio": green_ratio,
        "is_sprouted": is_sprouted,
        "dark_ratio": dark_ratio,
        "is_rotten": is_rotten,
        "edge_density": edge_density,
        "is_damaged": is_damaged,
    }
