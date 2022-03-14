#!/bin/bash

# https://wiki.alice.universiteitleiden.nl/index.php?title=Your_first_GPU_job
#SBATCH --output /home/uraiae/jobs/job_fit-%A_%a.out
#SBATCH --mail-user=a.e.urai@fsw.leidenuniv.nl # mail when done
#SBATCH --mail-type=END,FAIL # mail when done
#SBATCH -p testing # gpu-short
#SBATCH --ntasks=1
#SBATCH --gpus=1
#SBATCH --time=01:00:00 # one hour to fit

# load necessary modules
module load Miniconda3/4.9.2
source activate hddmnn_env  # for all installed packages
export PYTHONUNBUFFERED=TRUE # use -u to continually show output in logfile (unbuffered)

# are we using the GPU?
echo "[$SHELL] Using GPU: "$CUDA_VISIBLE_DEVICES
echo "[$SHELL]: "$DATE

# get the current working directory
export CWD=$(pwd)
echo "[$SHELL] CWD: "$CWD

# Set the path to the python file
export PATH_TO_PYFILE=$CWD
echo "[$SHELL] Path of python file: "$PATH_TO_PYFILE

# Set name of the python file
export PYFILE=$CWD/fit_simdata.py

# Create a directory of local scratch on the node
echo "[$SHELL] Node scratch: "$SCRATCH
export RUNDIR=$SCRATCH/test_tf
mkdir $RUNDIR
echo "[$SHELL] Run directory"$RUNDIR

# Create directory for plots
export DATADIR=$RUNDIR/data

# copy script to local scratch directory and change into it
cp $PYFILE $RUNDIR/
cd $RUNDIR

# Actuall run the file
python fit_simdata.py -m $SLURM_ARRAY_TASK_ID # run the number of arrays thats specified

# Move stat directory back to CWD
echo "[$SHELL] Copy files back to CWD"
cp -r $DATADIR $CWD/

# Wrap up
echo "[$SHELL]: Finished at " $DATE
