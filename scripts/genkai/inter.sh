#!/bin/bash
#  singularity exec --nv ubuntu.sif bash inter.sh

uv sync
uv pip install -e .
uv run python scripts/train.py
