import os
import random
from PIL import Image, ImageDraw, ImageFilter

CLASSES = ["healthy", "damaged", "rotten", "sprouted", "undersized"]
SPLITS = {"train": 30, "val": 10, "test": 10}
IMAGE_SIZE = (224, 224)

def generate_synthetic_onion(class_name: str) -> Image.Image:
    """Generates a synthetic onion image representing a defect class."""
    bg_color = (random.randint(230, 255), random.randint(220, 245), random.randint(210, 235))
    img = Image.new("RGB", IMAGE_SIZE, color=bg_color)
    draw = ImageDraw.Draw(img)

    # Base onion dimensions & position
    center_x, center_y = 112, 112
    radius = random.randint(55, 75) if class_name != "undersized" else random.randint(30, 45)

    # Base colors
    base_color = (218, 140, 60) # Typical onion skin reddish-brown
    inner_color = (240, 200, 150)

    # Draw main onion bulb
    bbox = [center_x - radius, center_y - radius, center_x + radius, center_y + radius]
    draw.ellipse(bbox, fill=base_color, outline=(150, 80, 30), width=2)
    draw.ellipse([center_x - radius + 10, center_y - radius + 10, center_x + radius - 10, center_y + radius - 10], fill=inner_color)

    # Defect specific alterations
    if class_name == "damaged":
        # Mechanical cuts/cracks (dark brown lines)
        for _ in range(3):
            x1 = center_x + random.randint(-radius//2, radius//2)
            y1 = center_y + random.randint(-radius//2, radius//2)
            x2 = x1 + random.randint(-20, 20)
            y2 = y1 + random.randint(-20, 20)
            draw.line([(x1, y1), (x2, y2)], fill=(60, 30, 10), width=4)

    elif class_name == "rotten":
        # Dark blackish soft rot decay patch
        rot_radius = random.randint(15, 30)
        rot_x = center_x + random.randint(-radius//3, radius//3)
        rot_y = center_y + random.randint(-radius//3, radius//3)
        draw.ellipse([rot_x - rot_radius, rot_y - rot_radius, rot_x + rot_radius, rot_y + rot_radius], fill=(40, 30, 20))

    elif class_name == "sprouted":
        # Green shoot emerging top apical node
        shoot_top = center_y - radius - random.randint(25, 45)
        shoot_x = center_x + random.randint(-10, 10)
        draw.polygon([(center_x - 8, center_y - radius + 5), (center_x + 8, center_y - radius + 5), (shoot_x, shoot_top)], fill=(40, 160, 40))

    return img.filter(ImageFilter.SMOOTH)

def create_dataset(output_dir: str = "ml/dataset"):
    """Creates the dataset directory structure and populates synthetic onion images."""
    os.makedirs(output_dir, exist_ok=True)
    total_generated = 0

    for split, count in SPLITS.items():
        for c in CLASSES:
            class_dir = os.path.join(output_dir, split, c)
            os.makedirs(class_dir, exist_ok=True)
            for i in range(count):
                img = generate_synthetic_onion(c)
                file_path = os.path.join(class_dir, f"{c}_{i+1:03d}.jpg")
                img.save(file_path, "JPEG")
                total_generated += 1

    print(f"[Dataset Generator] Successfully generated {total_generated} synthetic images in '{output_dir}'.")
    print(f"[Dataset Generator] Classes: {CLASSES}")
    print(f"[Dataset Generator] Splits: {SPLITS}")

if __name__ == "__main__":
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset"))
    create_dataset(base_path)
