# ML Training Pipeline & AIDE ML Agent Integration for OnionIQ

This directory provides the machine learning experimentation and training pipeline for fine-tuning Deep Learning models (e.g., ResNet18 / MobileNetV3 / EfficientNet) for onion quality defect classification.

It includes integration with **AIDE ML** (`wecoai/aideml`), an autonomous LLM tree-search agent that builds, tests, and optimizes ML models iteratively.

---

## Dataset Structure

Organize dataset images into class folders:

```
ml/dataset/
├── train/
│   ├── healthy/
│   ├── damaged/
│   ├── rotten/
│   ├── sprouted/
│   └── undersized/
├── val/
│   ├── healthy/
│   ├── damaged/
│   ├── rotten/
│   ├── sprouted/
│   └── undersized/
└── test/
    ├── healthy/
    ├── damaged/
    ├── rotten/
    ├── sprouted/
    └── undersized/
```

### Quick Start: Generate Synthetic Dataset

Generate synthetic test images for immediate testing:

```bash
python generate_dataset.py
```

---

## Supported Defect Classes

1. **Healthy**: Uniform skin, no cuts/cracks/rot/sprouts.
2. **Damaged**: Mechanical cuts, bruised surfaces, skin cracks.
3. **Rotten**: Soft rot, dark blackish/brown decay patches.
4. **Sprouted**: Visible green shoot emergence from top apical node.
5. **Undersized**: Small diameter below procurement baseline.

---

## Running Autonomous Model Search with AIDE ML

Install required dependencies:

```bash
pip install -r requirements.txt
```

### 1. Validate Setup (Dry Run)

```bash
python run_aide.py --dry_run
```

### 2. Run AIDE Agentic Search

```bash
export OPENAI_API_KEY="<your-api-key>"

# Run via python script harness
python run_aide.py --data_dir dataset/ --steps 10 --code_model gpt-4o

# Or run directly via AIDE CLI
aide data_dir="dataset/" goal="Classify onion defect images into healthy, damaged, rotten, sprouted, and undersized" eval="Macro F1-Score"
```

Best solution code will be saved to `logs/<run_id>/best_solution.py` and exported to `backend/app/services/classifier/models/best_aide_solution.py`.

---

## Standard Training Commands

```bash
# Manual training script
python train.py --data_dir dataset/ --epochs 25 --arch resnet18 --output models/onion_defect_resnet18.pth
```
