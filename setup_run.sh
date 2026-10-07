#!/bin/bash

set -e

CONFIG=${1:-configs/grn.yaml}

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

pip install -e .

echo "Running PaperPilot with: $CONFIG"
python scripts/run.py --config "$CONFIG"

