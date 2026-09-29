import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Union

try:
    import torch
    import torchvision.transforms as transforms
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)
TARGET_SIZE = (224, 224)
FILL_COLOR = (235, 230, 225)  # Neutral background fill matching dataset baseline


def letterbox_image_np(
    image_bgr: np.ndarray,
    target_size: Tuple[int, int] = TARGET_SIZE,
    fill_color: Tuple[int, int, int] = FILL_COLOR
) -> np.ndarray:
    """
    Pads an image to a square aspect ratio without distortion,
    then resizes to target_size (width, height).
    Returns RGB uint8 image.
    """
    h, w = image_bgr.shape[:2]
    tw, th = target_size

    # Convert BGR to RGB
    img_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    # Uniform scale factor preserving aspect ratio
    scale = min(tw / w, th / h)
    nw, nh = int(round(w * scale)), int(round(h * scale))

    # Bilinear interpolation
    resized = cv2.resize(img_rgb, (nw, nh), interpolation=cv2.INTER_LINEAR)

    # Create letterbox canvas
    canvas = np.full((th, tw, 3), fill_color, dtype=np.uint8)
    pad_top = (th - nh) // 2
    pad_left = (tw - nw) // 2
    canvas[pad_top:pad_top + nh, pad_left:pad_left + nw] = resized

    return canvas


def letterbox_image_pil(
    pil_img: Image.Image,
    target_size: Tuple[int, int] = TARGET_SIZE,
    fill_color: Tuple[int, int, int] = FILL_COLOR
) -> Image.Image:
    """
    PIL-based letterbox preserving aspect ratio and centering image.
    """
    img = pil_img.convert("RGB")
    w, h = img.size
    tw, th = target_size

    scale = min(tw / w, th / h)
    nw, nh = int(round(w * scale)), int(round(h * scale))

    resized = img.resize((nw, nh), Image.Resampling.BILINEAR)

    canvas = Image.new("RGB", (tw, th), fill_color)
    pad_left = (tw - nw) // 2
    pad_top = (th - nh) // 2
    canvas.paste(resized, (pad_left, pad_top))

    return canvas


def preprocess_for_inference_np(
    image_bgr: np.ndarray,
    target_size: Tuple[int, int] = TARGET_SIZE
) -> np.ndarray:
    """
    Preprocesses a BGR image into an NCHW [1, 3, 224, 224] float32 tensor
    with ImageNet mean & std normalization.
    """
    # 1. Aspect-ratio preserving letterbox + RGB conversion
    canvas = letterbox_image_np(image_bgr, target_size=target_size)

    # 2. Rescale [0, 255] -> [0.0, 1.0]
    normalized = canvas.astype(np.float32) / 255.0

    # 3. ImageNet standard normalization (mean & std)
    normalized = (normalized - IMAGENET_MEAN) / IMAGENET_STD

    # 4. Transpose HWC -> CHW -> NCHW [1, 3, H, W]
    chw = np.transpose(normalized, (2, 0, 1))
    nchw = np.expand_dims(chw, axis=0)

    return nchw


def preprocess_for_inference_torch(
    pil_image: Image.Image,
    target_size: Tuple[int, int] = TARGET_SIZE
) -> "torch.Tensor":
    """
    PyTorch inference preprocessing producing [1, 3, 224, 224] float32 tensor.
    """
    if not HAS_TORCH:
        raise ImportError("PyTorch is required for preprocess_for_inference_torch.")

    canvas = letterbox_image_pil(pil_image, target_size=target_size)

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    tensor = transform(canvas).unsqueeze(0)  # Shape: [1, 3, 224, 224], dtype: torch.float32
    return tensor
