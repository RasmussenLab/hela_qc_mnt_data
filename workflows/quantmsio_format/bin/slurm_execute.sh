#!/bin/bash
# The number of CPUs (cores) used by your task. Defaults to 1.
#SBATCH --cpus-per-task=10
# The amount of RAM used by your task. Tasks are automatically assigned 15G
# per CPU (set above) if this option is not set.
#SBATCH --mem=256G
# Set a maximum runtime in hours:minutes:seconds. No default limit.
#SBATCH --time=03:00:00
# Request a GPU on the GPU code. Use `--gres=gpu:a100:2` to request both GPUs.
##SBATCH --partition=gpuqueue --gres=gpu:a100:1
# Send notifications when job ends. Remember to update the email address!
##SBATCH --mail-user=abc123@ku.dk --mail-type=END,FAIL

set -o nounset  # Exit on unset variables
set -o pipefail # Exit on unhandled failure in pipes
set -o errtrace # Have functions inherit ERR traps

########################
# Your commands go here:
current_date=$(date +%Y-%m-%d_%H-%M)
echo Running in folder: "$PWD"

# check if bashrc is imported
conda info -e # List all conda environments

snakemake -c4 --rerun-incomplete -n -p --rerun-triggers mtime > "snakemake_dryrun_$current_date.log"
snakemake -c16 --rerun-incomplete -q rules -n --rerun-triggers mtime
snakemake -c16 --rerun-incomplete -k --use-conda --conda-frontend conda --rerun-triggers mtime
echo Done