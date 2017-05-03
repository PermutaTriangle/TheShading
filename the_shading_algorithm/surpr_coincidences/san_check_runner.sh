#!/bin/bash

#SBATCH --job-name=TSA_sancheck
#SBATCH --output=tsa_sancheck_%A_%a.out
#SBATCH --error=tsa_sanchec_%A_%a.err
#SBATCH --array=1-10

perms=$(head -n $SLURM_ARRAY_TASK_ID active_021.txt | tail -n -1)
python3 sanity_checker.py 13 "0 2 1" $perms
