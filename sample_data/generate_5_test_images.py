import cv2
import numpy as np
from pathlib import Path

def generate_5_images():
    out_dir = Path(__file__).parent
    w, h = 1024, 768

    # 1. Dark/Purple & Dirty Onions on Cardboard Background
    img1 = np.ones((h, w, 3), dtype=np.uint8)
    img1[:, :] = (140, 160, 180)  # Cardboard brown/tan surface
    # Draw cardboard texture lines
    for i in range(0, w, 40):
        cv2.line(img1, (i, 0), (i, h), (130, 150, 170), 1)

    onions1 = [
        (200, 220, 75, (70, 40, 90)),   # Dark purple onion
        (450, 200, 80, (60, 30, 85)),   # Dark purple onion
        (720, 240, 70, (65, 35, 80)),   # Dark purple onion
        (250, 500, 85, (55, 25, 75)),   # Dirty dark onion
        (520, 520, 75, (75, 45, 95)),   # Dark purple onion
        (800, 510, 65, (60, 30, 80)),   # Purple onion
    ]
    for x, y, r, c in onions1:
        cv2.circle(img1, (x+6, y+6), r, (80, 100, 110), -1)  # Shadow
        cv2.circle(img1, (x, y), r, c, -1)
        cv2.circle(img1, (x, y), r, (30, 10, 40), 3)

    cv2.imwrite(str(out_dir / "test_img1_purple_cardboard.jpg"), img1)

    # 2. Yellow Onions on Wooden Tray
    img2 = np.ones((h, w, 3), dtype=np.uint8)
    img2[:, :] = (100, 130, 160)  # Wooden brown
    onions2 = [
        (180, 200, 70, (30, 160, 210)),  # Golden yellow
        (400, 220, 78, (25, 150, 200)),
        (650, 190, 82, (35, 170, 220)),
        (860, 230, 68, (28, 155, 205)),
        (300, 500, 75, (30, 160, 210)),
        (600, 520, 80, (25, 150, 200)),
    ]
    for x, y, r, c in onions2:
        cv2.circle(img2, (x+5, y+5), r, (60, 80, 100), -1)
        cv2.circle(img2, (x, y), r, c, -1)
        cv2.circle(img2, (x, y), r, (15, 90, 140), 3)

    cv2.imwrite(str(out_dir / "test_img2_yellow_wood.jpg"), img2)

    # 3. Overlapping Onions on Metal Conveyor
    img3 = np.ones((h, w, 3), dtype=np.uint8) * 190  # Metal gray
    for j in range(0, h, 60):
        cv2.line(img3, (0, j), (w, j), (160, 160, 160), 2)
    onions3 = [
        (220, 250, 75, (40, 80, 180)),
        (320, 260, 72, (35, 75, 175)),  # Overlapping with previous
        (550, 240, 80, (45, 85, 185)),
        (750, 270, 78, (30, 70, 170)),
        (400, 500, 70, (40, 80, 180)),
        (620, 480, 85, (35, 75, 175)),
    ]
    for x, y, r, c in onions3:
        cv2.circle(img3, (x+4, y+4), r, (120, 120, 120), -1)
        cv2.circle(img3, (x, y), r, c, -1)
        cv2.circle(img3, (x, y), r, (20, 40, 90), 3)

    cv2.imwrite(str(out_dir / "test_img3_metal_conveyor.jpg"), img3)

    # 4. Red Onions with Green Sprouts
    img4 = np.ones((h, w, 3), dtype=np.uint8) * 220
    onions4 = [
        (200, 220, 75, (40, 60, 170)),
        (450, 210, 80, (45, 65, 175)),
        (700, 230, 70, (35, 55, 165)),
        (300, 500, 78, (40, 60, 170)),
        (600, 510, 82, (45, 65, 175)),
    ]
    for x, y, r, c in onions4:
        cv2.circle(img4, (x, y), r, c, -1)
        # Green sprout shoots
        pts = np.array([[x-12, y-r+5], [x+12, y-r+5], [x, y-r-50]], np.int32)
        cv2.fillPoly(img4, [pts], (30, 170, 40))

    cv2.imwrite(str(out_dir / "test_img4_sprouted_red.jpg"), img4)

    # 5. Standard Mixed Tray
    img5 = np.ones((h, w, 3), dtype=np.uint8) * 230
    onions5 = [
        (180, 200, 75, (40, 80, 180)),
        (400, 180, 82, (35, 75, 175)),
        (650, 220, 70, (45, 85, 185)),
        (850, 240, 78, (30, 70, 170)),
        (220, 480, 80, (20, 40, 90)),
        (460, 500, 68, (50, 100, 190)),
        (700, 490, 76, (40, 80, 180)),
        (900, 520, 42, (38, 78, 178)),
    ]
    for x, y, r, c in onions5:
        cv2.circle(img5, (x, y), r, c, -1)

    cv2.imwrite(str(out_dir / "test_img5_mixed_tray.jpg"), img5)

    print("Successfully generated 5 diverse onion batch test images in sample_data/!")

if __name__ == '__main__':
    generate_5_images()
