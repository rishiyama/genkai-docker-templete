#!/bin/bash
#  singularity exec --nv ubuntu.sif bash inter.sh

cd /workspace/
uv sync
uv pip install -e .
source .venv/bin/activate
which python
python scripts/train.py
