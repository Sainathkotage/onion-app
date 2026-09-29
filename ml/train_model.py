import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms

CLASSES = ["healthy", "damaged", "rotten", "sprouted", "undersized"]
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset"))
OUTPUT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "models/densenet121_onion.pth"))

from PIL import Image

class LetterboxSquare:
    """Aspect-ratio preserving letterbox transform to 1:1 square canvas."""
    def __init__(self, size: int = 224, fill: tuple = (235, 230, 225)):
        self.size = size
        self.fill = fill

    def __call__(self, img: Image.Image) -> Image.Image:
        img = img.convert("RGB")
        w, h = img.size
        scale = min(self.size / w, self.size / h)
        nw, nh = int(round(w * scale)), int(round(h * scale))
        resized = img.resize((nw, nh), Image.Resampling.BILINEAR)
        canvas = Image.new("RGB", (self.size, self.size), self.fill)
        pad_left = (self.size - nw) // 2
        pad_top = (self.size - nh) // 2
        canvas.paste(resized, (pad_left, pad_top))
        return canvas

def train_model(epochs: int = 2):
    print("=" * 70)
    print("      OnionIQ - DenseNet-121 Deep Learning Training Pipeline")
    print("=" * 70)
    print(f"[ML Train] Loading dataset from : {DATA_DIR}")
    print(f"[ML Train] Output Model Path   : {OUTPUT_PATH}")
    print(f"[ML Train] Classes             : {CLASSES}")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Image Transforms matching inference preprocessing
    data_transforms = {
        'train': transforms.Compose([
            LetterboxSquare(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            LetterboxSquare(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    # Load datasets
    image_datasets = {}
    for x in ['train', 'val']:
        split_dir = os.path.join(DATA_DIR, x)
        if os.path.exists(split_dir):
            image_datasets[x] = datasets.ImageFolder(split_dir, data_transforms[x])

    if not image_datasets:
        print("[ML Train Error] Dataset split directories not found. Run `python generate_dataset.py` first.")
        return

    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=8, shuffle=True) for x in image_datasets}
    dataset_sizes = {x: len(image_datasets[x]) for x in image_datasets}

    device = torch.device("cpu")
    print(f"[ML Train] Training on device: {device}")

    # Build DenseNet-121 model structure
    model = models.densenet121(weights=None)
    num_ftrs = model.classifier.in_features
    model.classifier = nn.Linear(num_ftrs, len(CLASSES))
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(epochs):
        print(f"\n[ML Train] Epoch {epoch + 1}/{epochs}")
        print("-" * 30)

        for phase in ['train', 'val']:
            if phase not in dataloaders:
                continue
            model.train() if phase == 'train' else model.eval()

            running_loss = 0.0
            running_corrects = 0

            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]
            print(f"{phase.capitalize()} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")

    # Save model state dict
    torch.save(model.state_dict(), OUTPUT_PATH)
    print("=" * 70)
    print(f"[ML Train] Model trained successfully! Saved weights to:")
    print(f"           '{OUTPUT_PATH}'")
    print("=" * 70)

if __name__ == '__main__':
    train_model(epochs=2)
