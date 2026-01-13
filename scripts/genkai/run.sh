#!/bin/sh

#PJM -L rscgrp=b-batch
#PJM -L gpu=1
#PJM -L elapse=0:10:00
#PJM -L jobenv=singularity
#PJM -j

module load cuda/11.8.0
module load singularity-ce/4.1.3
singularity exec ubuntu.sif bash scripts/genkai/inter.sh