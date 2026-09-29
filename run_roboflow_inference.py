#!/usr/bin/env python3
"""
Roboflow Serverless Cloud Inference Script for Onion Quality Assessment.
Model: onion-disease/3
API: https://serverless.roboflow.com
Authentication: Header-based Bearer token (Inference v1.5.0+)
"""

import os
import sys
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
load_dotenv(Path(__file__).parent / "backend" / ".env")

try:
    from inference_sdk import InferenceHTTPClient, InferenceConfiguration
except ImportError:
    print("Error: inference-sdk is not installed. Install with: pip install inference-sdk")
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run inference using Roboflow model 'onion-disease/3' on an image."
    )
    parser.add_argument(
        "--image",
        type=str,
        default="sample_data/test_img1_purple_cardboard.jpg",
        help="Path to the image file (local path or public image URL)."
    )
    parser.add_argument(
        "--model_id",
        type=str,
        default=os.getenv("ROBOFLOW_MODEL_ID", "onion-disease/3"),
        help="Roboflow model ID (default: onion-disease/3)."
    )
    parser.add_argument(
        "--api_url",
        type=str,
        default=os.getenv("ROBOFLOW_API_URL", "https://serverless.roboflow.com"),
        help="Roboflow Serverless API URL."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="sample_data/roboflow_output_annotated.jpg",
        help="Path to save annotated output image (for local files)."
    )
    return parser.parse_args()


def run_inference(image_input: str, model_id: str, api_url: str, output_path: str = None):
    api_key = os.getenv("ROBOFLOW_API_KEY")
    if not api_key:
        print("Error: ROBOFLOW_API_KEY environment variable is not set.")
        print("Please configure ROBOFLOW_API_KEY in your .env file or environment.")
        sys.exit(1)

    print(f"=== Roboflow Model Inference ===")
    print(f"Model ID: {model_id}")
    print(f"API URL : {api_url}")
    print(f"Target  : {image_input}")
    print(f"Auth    : Header-based Bearer authentication (inference v1.5.0+)")

    client = InferenceHTTPClient(
        api_url=api_url,
        api_key=api_key
    ).configure(InferenceConfiguration(
        api_key_transport="header"
    ))

    result = client.infer(image_input, model_id=model_id)

    print("\n--- Inference Result JSON ---")
    print(json.dumps(result, indent=2))

    predictions = result.get("predictions", [])
    print(f"\nTotal detections: {len(predictions)}")
    for idx, pred in enumerate(predictions, 1):
        cls = pred.get("class", "unknown")
        conf = pred.get("confidence", 0.0)
        cx, cy = pred.get("x", 0), pred.get("y", 0)
        w, h = pred.get("width", 0), pred.get("height", 0)
        print(f"  #{idx}: [{cls}] confidence={conf:.2f} center=({cx:.1f}, {cy:.1f}) size=({w:.1f}x{h:.1f})")

    # If image is local file, render annotated visualization
    local_img_path = Path(image_input)
    if local_img_path.exists() and output_path:
        try:
            import cv2
            img = cv2.imread(str(local_img_path))
            if img is not None:
                img_h, img_w = img.shape[:2]
                for idx, pred in enumerate(predictions, 1):
                    cx, cy = float(pred["x"]), float(pred["y"])
                    bw, bh = float(pred["width"]), float(pred["height"])
                    x1 = max(0, int(cx - bw / 2))
                    y1 = max(0, int(cy - bh / 2))
                    x2 = min(img_w, int(cx + bw / 2))
                    y2 = min(img_h, int(cy + bh / 2))
                    cls = pred.get("class", "onion")
                    conf = float(pred.get("confidence", 0.0))

                    cv2.rectangle(img, (x1, y1), (x2, y2), (46, 175, 110), 3)
                    label = f"{cls} #{idx} ({conf:.0%})"
                    cv2.putText(img, label, (x1, max(15, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (46, 175, 110), 2)

                out_p = Path(output_path)
                out_p.parent.mkdir(parents=True, exist_ok=True)
                cv2.imwrite(str(out_p), img)
                print(f"\nAnnotated visualization saved to: {out_p}")
        except Exception as e:
            print(f"Note: Could not create annotated visualization: {e}")

    return result


if __name__ == "__main__":
    args = parse_args()
    run_inference(args.image, args.model_id, args.api_url, args.output)
