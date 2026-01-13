#!/bin/bash
#  singularity exec --nv ubuntu.sif bash inter.sh

uv sync
uv pip install -e .
source .venv/bin/activate
which python
python scripts/train.py
