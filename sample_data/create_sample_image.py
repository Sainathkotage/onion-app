import cv2
import numpy as np
from pathlib import Path

def generate_sample_onion_tray(output_path: str):
    # Create background tray (light beige/gray tray surface)
    width, height = 1024, 768
    img = np.ones((height, width, 3), dtype=np.uint8) * 230
    
    # Draw tray border
    cv2.rectangle(img, (20, 20), (width - 20, height - 20), (180, 180, 180), 8)
    cv2.rectangle(img, (30, 30), (width - 30, height - 30), (210, 210, 210), -1)

    # Define positions for 8 sample onions
    onions = [
        # (x, y, radius, color (BGR), defect_type)
        (180, 200, 75, (40, 80, 180), "Healthy"),       # Classic reddish onion
        (400, 180, 82, (35, 75, 175), "Healthy"),
        (650, 220, 70, (45, 85, 185), "Healthy"),
        (850, 240, 78, (30, 70, 170), "Healthy"),
        (220, 480, 80, (20, 40, 90),  "Rotten"),        # Dark brownish rot spot
        (460, 500, 68, (50, 100, 190), "Damaged"),       # Cut/crack mark
        (700, 490, 76, (40, 80, 180), "Sprouted"),      # Green sprout on top
        (900, 520, 42, (38, 78, 178), "Undersized"),    # Small radius
    ]

    for x, y, r, color, label in onions:
        # Shadow
        cv2.circle(img, (x + 8, y + 8), r, (150, 150, 150), -1)
        # Main onion body
        cv2.circle(img, (x, y), r, color, -1)
        # Inner onion rings texture
        cv2.circle(img, (x - r//4, y - r//4), r//2, (color[0]+30, color[1]+30, color[2]+30), 3)
        cv2.circle(img, (x, y), r, (color[0]-20, color[1]-20, color[2]-20), 4)

        if label == "Rotten":
            # Dark rot patch
            cv2.circle(img, (x + 10, y + 10), r//2, (10, 20, 40), -1)
        elif label == "Damaged":
            # Cut line
            cv2.line(img, (x - r//2, y - r//3), (x + r//2, y + r//3), (20, 20, 40), 5)
        elif label == "Sprouted":
            # Green sprout tip
            pts = np.array([[x - 10, y - r + 5], [x + 10, y - r + 5], [x, y - r - 45]], np.int32)
            cv2.fillPoly(img, [pts], (30, 160, 40))

    cv2.imwrite(output_path, img)
    print(f"Generated sample onion tray image at: {output_path}")

if __name__ == "__main__":
    out_dir = Path(__file__).parent
    out_dir.mkdir(exist_ok=True)
    generate_sample_onion_tray(str(out_dir / "sample_onions_tray.jpg"))
