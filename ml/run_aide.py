"""
AIDE ML Integration Runner for OnionIQ ML Pipeline.
Invokes WecoAI/aideml to search for optimal machine learning code/architecture on onion defect dataset.
"""

import argparse
import os
import sys

def run_aide_experiment(data_dir: str, steps: int, code_model: str, dry_run: bool = False):
    print("=" * 70)
    print("      OnionIQ - AIDE ML Autonomous Experimentation Engine")
    print("=" * 70)
    print(f"[AIDE ML] Dataset Directory : {data_dir}")
    print(f"[AIDE ML] Search Steps      : {steps}")
    print(f"[AIDE ML] LLM Code Model    : {code_model}")
    print(f"[AIDE ML] Target Task       : Multi-class Onion Defect Classification")
    print(f"[AIDE ML] Target Classes    : ['healthy', 'damaged', 'rotten', 'sprouted', 'undersized']")
    print(f"[AIDE ML] Metric            : Macro F1-Score")
    print("-" * 70)

    if dry_run:
        print("[AIDE ML] Dry-run flag set. Validating configuration and dataset readiness...")
        if os.path.exists(data_dir):
            print(f"[AIDE ML] Dataset verified at '{data_dir}'. Ready to run AIDE agent.")
        else:
            print(f"[AIDE ML] Warning: Dataset not found at '{data_dir}'. Run `python generate_dataset.py` first.")
        print("[AIDE ML] Dry-run completed successfully.")
        return

    try:
        import aide
        print("[AIDE ML] Initializing AIDE Experiment...")
        exp = aide.Experiment(
            data_dir=data_dir,
            goal="Build a high-accuracy PyTorch image classifier for 5 onion defect categories: healthy, damaged, rotten, sprouted, undersized.",
            eval="Macro F1-Score"
        )
        best_solution = exp.run(steps=steps)
        print(f"\n[AIDE ML] Experiment complete! Best Validation Metric: {best_solution.valid_metric}")
        print("-" * 70)
        print("[AIDE ML] Best Generated Code Snippet:\n")
        print(best_solution.code[:500] + "..." if len(best_solution.code) > 500 else best_solution.code)
        
        # Copy / export best solution
        output_dir = os.path.abspath("../backend/app/services/classifier/models")
        os.makedirs(output_dir, exist_ok=True)
        best_code_path = os.path.join(output_dir, "best_aide_solution.py")
        with open(best_code_path, "w", encoding="utf-8") as f:
            f.write(best_solution.code)
        print(f"\n[AIDE ML] Exported best model solution code to: {best_code_path}")

    except ImportError:
        print("\n[AIDE ML Error] `aideml` package is not installed.")
        print("Please install aideml dependencies using:")
        print("    pip install -r requirements.txt")
        print("Or run using CLI:")
        print(f"    aide data_dir=\"{data_dir}\" goal=\"Classify onion defect images\" eval=\"Macro F1-Score\"")
        sys.exit(1)
    except Exception as e:
        print(f"\n[AIDE ML Error] Experiment failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run AIDE ML for OnionIQ Model Optimization")
    parser.add_argument('--data_dir', type=str, default='dataset/')
    parser.add_argument('--steps', type=int, default=5)
    parser.add_argument('--code_model', type=str, default='gpt-4o')
    parser.add_argument('--dry_run', action='store_true', help='Validate setup without running LLM search')
    args = parser.parse_args()

    run_aide_experiment(
        data_dir=args.data_dir,
        steps=args.steps,
        code_model=args.code_model,
        dry_run=args.dry_run
    )
