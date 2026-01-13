#!/bin/bash

#PJM -L rscgrp=b-batch
#PJM -L gpu=1
#PJM -L elapse=1:00:00
#PJM -j

# dockerhub image

DOCKER_IMAGE="ishiyamaryo/cuda11.8.0-ubuntu22.04-uv:v1.0"

module load cuda/11.8.0
module load cudnn
module load nccl
module load gcc
module load singularity-ce
