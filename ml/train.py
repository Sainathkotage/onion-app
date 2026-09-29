"""
Training script template for fine-tuning ResNet18 / MobileNetV3 on labeled onion defect dataset.
"""
import argparse

def train(data_dir: str, epochs: int, arch: str, output: str):
    print(f"[ML Train] Initializing training pipeline with architecture: {arch}")
    print(f"[ML Train] Loading datasets from: {data_dir}")
    print(f"[ML Train] Targets: ['Healthy', 'Damaged', 'Rotten', 'Sprouted', 'Undersized']")
    print("[ML Train] To run active training, populate ml/dataset/ with labeled images.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train Onion Defect Classifier")
    parser.add_argument('--data_dir', type=str, default='dataset/')
    parser.add_argument('--epochs', type=int, default=25)
    parser.add_argument('--arch', type=str, default='resnet18')
    parser.add_argument('--output', type=str, default='models/onion_defect_resnet18.pth')
    args = parser.parse_args()
    train(args.data_dir, args.epochs, args.arch, args.output)
