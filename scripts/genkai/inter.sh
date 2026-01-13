#!/bin/bash
#  singularity exec --nv ubuntu.sif bash inter.sh

uv sync
uv pip install -e .
source .venv/bin/activate
python scripts/train.py
