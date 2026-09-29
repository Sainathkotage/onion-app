import os
import cv2
import numpy as np
import traceback
from pathlib import Path
from app.services.detector.base_detector import BaseOnionDetector
from app.services.calibration.aruco_calibrator import ArucoCalibrator
from app.services.size.size_estimator import OnionSizeEstimator
from app.utils.image_processing import crop_and_save, draw_detection_annotations
from app.config import (
    UPLOAD_DIR,
    DEBUG_DIR,
    CONFIDENCE_THRESHOLD,
    IOU_THRESHOLD,
    MAX_ONION_AREA_RATIO,
    DEBUG_SAVE_PIPELINE
)

def compute_iou(boxA, boxB):
    """Computes IoU between two boxes [x1, y1, x2, y2]."""
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    inter_area = max(0, xB - xA) * max(0, yB - yA)
    areaA = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    areaB = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    union_area = float(areaA + areaB - inter_area)
    return inter_area / union_area if union_area > 0 else 0.0

def merge_overlapping_boxes(boxes, confidences, iou_thresh=0.35, containment_thresh=0.60):
    """Merges overlapping or heavily contained bounding boxes."""
    if not boxes:
        return [], []
    
    merged = []
    merged_confs = []
    used = [False] * len(boxes)

    for i in range(len(boxes)):
        if used[i]:
            continue
        cur_box = list(boxes[i])
        cur_conf = confidences[i]
        used[i] = True

        changed = True
        while changed:
            changed = False
            for j in range(len(boxes)):
                if used[j]:
                    continue
                other_box = boxes[j]
                iou = compute_iou(cur_box, other_box)

                # Check containment
                xA = max(cur_box[0], other_box[0])
                yA = max(cur_box[1], other_box[1])
                xB = min(cur_box[2], other_box[2])
                yB = min(cur_box[3], other_box[3])
                inter = max(0, xB - xA) * max(0, yB - yA)
                area_other = (other_box[2] - other_box[0]) * (other_box[3] - other_box[1])
                containment = inter / float(area_other) if area_other > 0 else 0.0

                if iou > iou_thresh or containment > containment_thresh:
                    # Merge boxes
                    cur_box[0] = min(cur_box[0], other_box[0])
                    cur_box[1] = min(cur_box[1], other_box[1])
                    cur_box[2] = max(cur_box[2], other_box[2])
                    cur_box[3] = max(cur_box[3], other_box[3])
                    cur_conf = max(cur_conf, confidences[j])
                    used[j] = True
                    changed = True

        merged.append(cur_box)
        merged_confs.append(cur_conf)

    return merged, merged_confs

class CVOnionDetector(BaseOnionDetector):
    """
    Robust Multi-Strategy Computer Vision Onion Segmenter.
    Applies resolution-invariant preprocessing, adaptive saliency masks,
    large morphological closing, peak watershed distance filtering,
    and NMS + containment merging to eliminate overcounting.
    """
    def __init__(
        self,
        min_area: int = 1200,
        max_area_ratio: float = MAX_ONION_AREA_RATIO,
        conf_threshold: float = CONFIDENCE_THRESHOLD,
        nms_threshold: float = IOU_THRESHOLD
    ):
        self.min_area = min_area
        self.max_area_ratio = max_area_ratio
        self.conf_threshold = conf_threshold
        self.nms_threshold = nms_threshold
        self.calibrator = ArucoCalibrator()
        self.size_estimator = OnionSizeEstimator()

    def detect(self, image_path: str, upload_id: str) -> dict:
        try:
            img_path = Path(image_path)
            if not img_path.exists():
                raise FileNotFoundError(f"Image not found at path: {image_path}")

            img = cv2.imread(str(img_path))
            if img is None:
                raise ValueError(f"Could not load image file: {image_path}")

            # 0. ArUco Metric Reference Calibration
            calibration_info = self.calibrator.detect_marker(img)

            orig_h, orig_w, _ = img.shape
            orig_area = orig_h * orig_w

            # 1. Resolution normalization to 1024 max dimension for scale-invariant segmentation
            max_dim = max(orig_h, orig_w)
            scale = 1024.0 / max_dim if max_dim > 1024 else 1.0
            if scale < 1.0:
                work_w = int(orig_w * scale)
                work_h = int(orig_h * scale)
                work_img = cv2.resize(img, (work_w, work_h), interpolation=cv2.INTER_AREA)
            else:
                work_w, work_h = orig_w, orig_h
                work_img = img.copy()

            work_area = work_h * work_w
            # Minimum onion area: at least 0.8% of the image or 1200px on working resolution
            min_area_thresh = max(1200, int(work_area * 0.008))
            max_area_thresh = int(work_area * self.max_area_ratio)

            metrics = {
                "total_candidates": 0,
                "rejected_by_area": 0,
                "rejected_by_shape": 0,
                "rejected_by_color": 0,
                "rejected_by_confidence": 0,
                "final_detections": 0
            }

            # 2. Preprocessing & Multi-Channel Saliency
            blurred = cv2.GaussianBlur(work_img, (9, 9), 0)
            lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

            _, A, B = cv2.split(lab)
            _, S, _ = cv2.split(hsv)

            A_diff = cv2.absdiff(A, 128)
            B_diff = cv2.absdiff(B, 128)
            chroma_saliency = cv2.add(A_diff, B_diff)

            bg_mean = cv2.GaussianBlur(gray, (51, 51), 0)
            local_contrast = cv2.absdiff(gray, bg_mean)

            _, mask_chroma = cv2.threshold(chroma_saliency, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            _, mask_contrast = cv2.threshold(local_contrast, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            _, mask_S = cv2.threshold(S, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Auto-invert if inverted polarity
            if cv2.countNonZero(mask_chroma) > (work_area * 0.50):
                mask_chroma = cv2.bitwise_not(mask_chroma)
            if cv2.countNonZero(mask_contrast) > (work_area * 0.50):
                mask_contrast = cv2.bitwise_not(mask_contrast)
            if cv2.countNonZero(mask_S) > (work_area * 0.50):
                mask_S = cv2.bitwise_not(mask_S)

            # Color-based saliency (Chroma in Lab + Saturation in HSV)
            color_saliency = cv2.bitwise_or(mask_chroma, mask_S)

            # If color saliency is strong (typical for red/yellow/sprouted onions), use it directly.
            # Only incorporate cleaned local contrast if color saliency is sparse (e.g. peeled white onions on neutral background).
            if cv2.countNonZero(color_saliency) > (work_area * 0.005):
                combined_saliency = color_saliency
            else:
                # Remove border/perimeter contours from contrast mask before fusing
                cnts_c, _ = cv2.findContours(mask_contrast.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cleaned_contrast = np.zeros_like(mask_contrast)
                for cc in cnts_c:
                    ca = cv2.contourArea(cc)
                    cbx, cby, cbw, cbh = cv2.boundingRect(cc)
                    if ca > 0.35 * work_area or (cbw > 0.92 * work_w and cbh > 0.92 * work_h):
                        continue
                    cv2.drawContours(cleaned_contrast, [cc], -1, 255, -1)
                combined_saliency = cv2.bitwise_or(color_saliency, cleaned_contrast)

            # 3. Enhanced Morphological Filtering to bridge skin textures/reflections
            kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
            kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17))
            opened = cv2.morphologyEx(combined_saliency, cv2.MORPH_OPEN, kernel_open, iterations=1)
            closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel_close, iterations=2)

            # 4. Extract Primary Candidate Contours from Closed Saliency Mask
            contours_binary, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            raw_contours_list = []

            # Check for merged / touching onions or full tray border swallowing items
            for cnt in contours_binary:
                c_area = cv2.contourArea(cnt)
                bx, by, bw, bh = cv2.boundingRect(cnt)

                # Check if contour is the outer tray perimeter / image border
                is_tray_border = (
                    c_area > 0.45 * work_area or
                    (bx <= 10 and by <= 10 and (bx + bw) >= work_w - 10 and (by + bh) >= work_h - 10)
                )

                if is_tray_border:
                    inner_mask = np.zeros(closed.shape, dtype=np.uint8)
                    cv2.drawContours(inner_mask, [cnt], -1, 255, -1)
                    # Erode outer 40px perimeter of the border
                    cv2.rectangle(inner_mask, (0, 0), (work_w, work_h), 0, 40)
                    inner_closed = cv2.bitwise_and(closed, inner_mask)
                    inner_cnts, _ = cv2.findContours(inner_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    for ic in inner_cnts:
                        if cv2.contourArea(ic) >= min_area_thresh:
                            raw_contours_list.append(ic)
                    continue

                if c_area < min_area_thresh:
                    continue

                aspect = float(bw) / bh if bh > 0 else 1.0
                if aspect > 2.4 or aspect < 0.42 or c_area > 0.25 * work_area:
                    mask_local = np.zeros(closed.shape, dtype=np.uint8)
                    cv2.drawContours(mask_local, [cnt], -1, 255, -1)
                    dt_local = cv2.distanceTransform(mask_local, cv2.DIST_L2, 5)
                    local_max = dt_local.max()
                    if local_max > 0:
                        _, local_peaks = cv2.threshold(dt_local, 0.45 * local_max, 255, 0)
                        n_lbl, _ = cv2.connectedComponents(np.uint8(local_peaks))
                        if n_lbl > 2:
                            peak_cnts, _ = cv2.findContours(np.uint8(local_peaks), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                            raw_contours_list.extend(peak_cnts)
                            continue
                raw_contours_list.append(cnt)

            metrics["total_candidates"] = len(raw_contours_list)

            raw_boxes = []
            raw_confs = []
            raw_boxes_for_debug = []

            # 5. Evaluate and Filter Contours
            for cnt in raw_contours_list:
                area = cv2.contourArea(cnt)
                x, y, bw, bh = cv2.boundingRect(cnt)

                # Scale coordinates back to original image space
                inv_scale = 1.0 / scale
                orig_x1 = max(0, int(x * inv_scale))
                orig_y1 = max(0, int(y * inv_scale))
                orig_x2 = min(orig_w, int((x + bw) * inv_scale))
                orig_y2 = min(orig_h, int((y + bh) * inv_scale))
                raw_boxes_for_debug.append([orig_x1, orig_y1, orig_x2, orig_y2])

                # Filter 1: Area threshold
                if area < min_area_thresh or area > max_area_thresh:
                    metrics["rejected_by_area"] += 1
                    continue

                # Filter 2: Aspect ratio (onions are roughly circular/oval: 0.40 to 2.5)
                aspect_ratio = float(bw) / bh if bh > 0 else 0
                if aspect_ratio < 0.40 or aspect_ratio > 2.5:
                    metrics["rejected_by_shape"] += 1
                    continue

                extent = float(area) / (bw * bh) if (bw * bh) > 0 else 0
                # Onions are elliptical/circular; maximum theoretical extent for an ellipse is pi/4 ~= 0.785.
                # Reject shapes with extent < 0.35 (thin slivers/lines) or extent > 0.82 (synthetic boxes, cards, rectangles).
                if extent < 0.35 or extent > 0.82:
                    metrics["rejected_by_shape"] += 1
                    continue

                # Filter 3: Reject synthetic flat geometric shapes (4-vertex polygons or flat color fields)
                peri = cv2.arcLength(cnt, True)
                if peri > 0:
                    approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
                    if len(approx) == 4 and extent > 0.80:
                        metrics["rejected_by_shape"] += 1
                        continue

                # Filter 4: Reject desaturated specular glare / white light reflections
                crop_hsv = hsv[y:y+bh, x:x+bw]
                if crop_hsv.size > 0 and float(np.mean(crop_hsv[:, :, 1])) < 25.0:
                    metrics["rejected_by_color"] += 1
                    continue

                # Solidity calculation
                hull = cv2.convexHull(cnt)
                hull_area = cv2.contourArea(hull)
                solidity = float(area) / hull_area if hull_area > 0 else 0.75
                confidence = round(float(min(0.99, max(0.60, solidity * 0.96))), 2)

                if confidence < self.conf_threshold:
                    metrics["rejected_by_confidence"] += 1
                    continue

                raw_boxes.append([orig_x1, orig_y1, orig_x2, orig_y2])
                raw_confs.append(confidence)

            # 6. Apply Containment Merging & Non-Maximum Suppression (NMS)
            merged_boxes, merged_confs = merge_overlapping_boxes(raw_boxes, raw_confs, iou_thresh=0.35, containment_thresh=0.55)

            boxes_for_cv_nms = []
            for b in merged_boxes:
                boxes_for_cv_nms.append([b[0], b[1], b[2] - b[0], b[3] - b[1]])

            final_onions = []
            if len(boxes_for_cv_nms) > 0:
                indices = cv2.dnn.NMSBoxes(boxes_for_cv_nms, merged_confs, self.conf_threshold, self.nms_threshold)
                if len(indices) > 0:
                    indices_list = indices.flatten() if isinstance(indices, np.ndarray) else indices
                    for idx_order, idx in enumerate(indices_list, start=1):
                        bbox = merged_boxes[idx]
                        conf = merged_confs[idx]
                        crop_path = crop_and_save(img, bbox, upload_id, idx_order)
                        label = f"Onion #{idx_order}"
                        bw = bbox[2] - bbox[0]
                        bh = bbox[3] - bbox[1]

                        final_onions.append({
                            "id": idx_order,
                            "label": label,
                            "bbox": bbox,
                            "confidence": conf,
                            "crop_path": crop_path,
                            "area": float(bw * bh),
                            "center": [bbox[0] + bw // 2, bbox[1] + bh // 2]
                        })

            # Sort onions top-to-bottom, left-to-right
            final_onions.sort(key=lambda item: (item["center"][1] // 100, item["center"][0]))
            for i, item in enumerate(final_onions, start=1):
                item["id"] = i
                item["label"] = f"Onion #{i}"

            metrics["final_detections"] = len(final_onions)

            # Calculate physical/relative size for each onion
            areas = [o["area"] for o in final_onions]
            median_area = float(np.median(areas)) if areas else 1000.0
            for o in final_onions:
                o["size"] = self.size_estimator.estimate_size(o["bbox"], o["area"], calibration_info, median_area)

            # Render Final Annotated Image (including ArUco marker overlay if present)
            annotated_img = draw_detection_annotations(img, final_onions, calibration_info)
            annotated_filename = f"{upload_id}_annotated.jpg"
            annotated_file_path = UPLOAD_DIR / annotated_filename
            cv2.imwrite(str(annotated_file_path), annotated_img)

            # 7. Save Debug Images if enabled
            if DEBUG_SAVE_PIPELINE:
                try:
                    cv2.imwrite(str(DEBUG_DIR / f"{upload_id}_1_original.jpg"), img)
                    debug_overlay = img.copy()
                    # Draw raw pre-filter boxes in red/orange
                    for rb in raw_boxes_for_debug:
                        cv2.rectangle(debug_overlay, (rb[0], rb[1]), (rb[2], rb[3]), (0, 140, 255), 2)
                    # Draw final merged boxes in green
                    for fo in final_onions:
                        fb = fo["bbox"]
                        cv2.rectangle(debug_overlay, (fb[0], fb[1]), (fb[2], fb[3]), (0, 255, 0), 3)
                    cv2.imwrite(str(DEBUG_DIR / f"{upload_id}_debug_overlay.jpg"), debug_overlay)
                except Exception as debug_err:
                    print(f"[CVDetector Debug Warning] Could not save debug files: {debug_err}")

            return {
                "upload_id": upload_id,
                "total_onions": len(final_onions),
                "annotated_image_url": f"/uploads/{annotated_filename}",
                "onions": final_onions,
                "raw_boxes": raw_boxes_for_debug,
                "detector_used": "Robust Scale-Invariant CV Onion Detector (NMS + Containment Merging)",
                "calibration": calibration_info,
                "debug_metrics": metrics,
                "status": "success"
            }
        except Exception as err:
            print("[CVDetector Error Exception Traceback]:")
            traceback.print_exc()
            raise err
