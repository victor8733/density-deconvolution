#!/bin/sh
#SBATCH -N 1      # nodes requested
#SBATCH -n 1      # tasks requested
#SBATCH --gres=gpu:1
#SBATCH --mem=14000  # memory in Mb
#SBATCH --time=0-05:00:00
#SBATCH -o output/sgd-%A_%a.txt  # send stdout to outfile
#SBATCH -e output/sgd_error-%A_%a.txt  # send stderr to errfile
#SBATCH --partition=apollo

source ~/.bashrc
conda activate deconv
python deconv/experiments/gaia/fit_gaia_lim_sgd.py -c 128 -b 500 -e 20 -l 0.01 -w=0.001 -k 10 --use-cuda data/gaia_sample_mag.npz results/sgd_${SLURM_JOBID}
