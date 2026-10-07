import argparse
import sys
from pathlib import Path


# Add the src/ directory to Python's import path.
ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

sys.path.insert(0, str(SRC_DIR))


from paperpilot.config import load_config
from paperpilot.pipeline import run_pipeline


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the PaperPilot literature-review pipeline."
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to the PaperPilot YAML configuration file.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    config = load_config(args.config)

    run_pipeline(config)


if __name__ == "__main__":
    main()