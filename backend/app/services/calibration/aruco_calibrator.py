import cv2
import numpy as np
from typing import Dict, Any, Optional, Tuple
from app.config import REFERENCE_MARKER_WIDTH_MM, ARUCO_DICT_NAME

class ArucoCalibrator:
    """
    Computer Vision Fiducial Marker Calibrator.
    Detects ArUco reference markers to calculate a metric scale (pixels per millimeter).
    Guarantees that physical millimeter dimensions are never fabricated without a verified physical marker.
    """
    ARUCO_DICTIONARIES = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
        "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
        "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
        "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
        "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
        "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    }

    def __init__(
        self,
        reference_width_mm: float = REFERENCE_MARKER_WIDTH_MM,
        dict_name: str = ARUCO_DICT_NAME
    ):
        self.reference_width_mm = reference_width_mm
        self.dict_id = self.ARUCO_DICTIONARIES.get(dict_name, cv2.aruco.DICT_4X4_50)
        self.dictionary = cv2.aruco.getPredefinedDictionary(self.dict_id)
        self.detector_params = cv2.aruco.DetectorParameters()
        
        # Adaptive thresholding for robustness across lighting
        self.detector_params.adaptiveThreshWinSizeMin = 3
        self.detector_params.adaptiveThreshWinSizeMax = 23
        self.detector_params.adaptiveThreshWinSizeStep = 10
        self.detector_params.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX

        self.detector = cv2.aruco.ArucoDetector(self.dictionary, self.detector_params)

    def detect_marker(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Detects an ArUco marker in the input image and calculates metric scale (pixels per mm).
        Returns a structured calibration object.
        """
        if image is None or image.size == 0:
            return self._uncalibrated_result("Invalid or empty image.")

        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        corners, ids, _ = self.detector.detectMarkers(gray)

        if ids is None or len(ids) == 0:
            return self._uncalibrated_result("Reference marker not detected in image.")

        # Select primary marker (first detected or largest area)
        best_idx = 0
        max_perimeter = 0.0
        parsed_corners = []

        for i, corner_set in enumerate(corners):
            pts = corner_set[0]  # Shape (4, 2)
            # Calculate 4 side lengths
            s1 = float(np.linalg.norm(pts[0] - pts[1]))
            s2 = float(np.linalg.norm(pts[1] - pts[2]))
            s3 = float(np.linalg.norm(pts[2] - pts[3]))
            s4 = float(np.linalg.norm(pts[3] - pts[0]))
            perim = s1 + s2 + s3 + s4
            if perim > max_perimeter:
                max_perimeter = perim
                best_idx = i
                parsed_corners = [s1, s2, s3, s4]

        # Reject degenerate/microscopic marker noise (< 20px perimeter)
        if max_perimeter < 20.0:
            return self._uncalibrated_result("Detected marker is too small or occluded for reliable scale.")

        chosen_pts = corners[best_idx][0]
        marker_id = int(ids[best_idx][0])

        s1, s2, s3, s4 = parsed_corners
        mean_side_px = float(max_perimeter / 4.0)

        # Perspective distortion metric: difference between longest and shortest edge relative to mean
        edge_lengths = [s1, s2, s3, s4]
        distortion_ratio = float((max(edge_lengths) - min(edge_lengths)) / mean_side_px) if mean_side_px > 0 else 0.0

        # Calibration scale
        pixels_per_mm = float(mean_side_px / self.reference_width_mm)

        center_x = float(np.mean(chosen_pts[:, 0]))
        center_y = float(np.mean(chosen_pts[:, 1]))

        # Corners as list of [x, y]
        corner_coords = [[round(float(pt[0]), 1), round(float(pt[1]), 1)] for pt in chosen_pts]

        perspective_warning = None
        if distortion_ratio > 0.22:
            perspective_warning = (
                f"Perspective tilt detected (edge ratio variance {distortion_ratio*100:.1f}%). "
                "Hold the camera perpendicular to the tray for optimal accuracy."
            )

        return {
            "status": "calibrated",
            "is_calibrated": True,
            "pixels_per_mm": round(pixels_per_mm, 4),
            "reference_width_mm": self.reference_width_mm,
            "marker_id": marker_id,
            "marker_side_pixels": round(mean_side_px, 1),
            "marker_center": [round(center_x, 1), round(center_y, 1)],
            "marker_corners": corner_coords,
            "distortion_ratio": round(distortion_ratio, 3),
            "perspective_warning": perspective_warning,
            "message": f"Calibrated via ArUco #{marker_id} ({round(pixels_per_mm, 2)} px/mm, {self.reference_width_mm}mm reference)."
        }

    def _uncalibrated_result(self, reason: str) -> Dict[str, Any]:
        return {
            "status": "not_calibrated",
            "is_calibrated": False,
            "pixels_per_mm": None,
            "reference_width_mm": self.reference_width_mm,
            "marker_id": None,
            "marker_side_pixels": None,
            "marker_center": None,
            "marker_corners": None,
            "distortion_ratio": None,
            "perspective_warning": None,
            "message": f"Calibration unavailable: {reason} Relative sizing active."
        }

    def annotate_marker(self, img: np.ndarray, calibration_info: Dict[str, Any]) -> np.ndarray:
        """
        Draws the detected ArUco marker boundary, coordinate vertices, and scale HUD on the image.
        """
        if not calibration_info.get("is_calibrated") or not calibration_info.get("marker_corners"):
            return img

        annotated = img.copy()
        corners = np.array(calibration_info["marker_corners"], dtype=np.int32)

        # Draw marker polygon (cyan/green)
        cv2.polylines(annotated, [corners], isClosed=True, color=(0, 255, 200), thickness=2)

        # Draw corner dots
        for pt in corners:
            cv2.circle(annotated, tuple(pt), 4, (0, 180, 255), -1)

        # Draw calibration badge text
        px_mm = calibration_info["pixels_per_mm"]
        marker_id = calibration_info["marker_id"]
        ref_mm = calibration_info["reference_width_mm"]
        cx, cy = int(calibration_info["marker_center"][0]), int(calibration_info["marker_center"][1])

        label = f"ArUco #{marker_id} ({px_mm:.2f} px/mm | {ref_mm}mm)"
        
        # Position label above marker
        text_pos = (max(10, cx - 100), max(25, cy - 35))
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        cv2.rectangle(
            annotated,
            (text_pos[0] - 4, text_pos[1] - th - 4),
            (text_pos[0] + tw + 4, text_pos[1] + 4),
            (20, 25, 30),
            -1
        )
        cv2.putText(
            annotated,
            label,
            text_pos,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 200),
            1,
            cv2.LINE_AA
        )

        return annotated

    def generate_sample_marker(self, marker_id: int = 0, side_pixels: int = 300) -> np.ndarray:
        """Generates a standalone ArUco marker image for testing or printing."""
        return cv2.aruco.generateImageMarker(self.dictionary, id=marker_id, sidePixels=side_pixels)
