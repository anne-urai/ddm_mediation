#!/bin/bash

# https://wiki.alice.universiteitleiden.nl/index.php?title=Running_jobs_on_ALICE
#SBATCH -p testing # gpu-short
# #SBATCH --gres=gpu:1
#SBATCH -t 1:00:00 # maximum 5 days on cartesius
#SBATCH --output /home/uraiae/jobs/job_lavaan-%A.out
#SBATCH --mail-user=a.e.urai@fsw.leidenuniv.nl # mail when done
#SBATCH --mail-type=END,FAIL # mail when done

# load necessary modules
module load Miniconda3/4.9.2
source activate hddmnn_env  # for all installed packages

# do something
date; hostname

# fit with lavaan
module load R/4.0.5-foss-2020b
Rscript fit_lavaan.R

date

