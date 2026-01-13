#!/bin/bash
#  singularity exec --nv ubuntu.sif bash inter.sh

uv sync
uv pip install -e .
uv python scripts/train.py
