#!/bin/bash

# https://wiki.alice.universiteitleiden.nl/index.php?title=Running_jobs_on_ALICE
#SBATCH -p testing # gpu-short
# #SBATCH --gres=gpu:1
#SBATCH -t 1:00:00 # maximum 5 days on cartesius
#SBATCH --output /home/uraiae/jobs/job_generate-%A.out
#SBATCH --mail-user=a.e.urai@fsw.leidenuniv.nl # mail when done
#SBATCH --mail-type=END,FAIL # mail when done

# load necessary modules
module load Miniconda3/4.9.2
source activate hddmnn_env  # for all installed packages
export PYTHONUNBUFFERED=TRUE # use -u to continually show output in logfile (unbuffered)

# do something
date; hostname

echo "starting python job"
python generate_data.py -m $SLURM_ARRAY_TASK_ID # run the number of arrays thats specified
date
