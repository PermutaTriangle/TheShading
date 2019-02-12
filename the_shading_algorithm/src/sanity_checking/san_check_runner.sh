#!/bin/bash

#SBATCH --job-name=TSA_sancheck
#SBATCH --array=1-2
#SBATCH --output=logs/tsa_sancheck_%A_%a.out
#SBATCH --error=logs/tsa_sancheck_%A_%a.err

module load python
source ~/permenv/bin/activate
perms=$(head -n $SLURM_ARRAY_TASK_ID active_021.txt | tail -n -1)
python3 sanity_checker.py 13 "0 2 1" $perms
