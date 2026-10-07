#!/bin/bash
#“#SBATCH” directives that convey submission options:

##### The name of the job
#SBATCH -J mace-lmps                # Job name
#SBATCH -o output.o%j               # output and error file name (%j expands to jobID)
#SBATCH -e output.e%j               # Name of stderr error file
#SBATCH -p gpu-h100                 # queue (partition) 
#SBATCH -N 1                        # number of nodes requested
#SBATCH -n 1                        # total number of tasks to run in parallel
#SBATCH --cpus-per-task=16          # Use 16 CPU cores for data loading
#SBATCH -t 24:00:00                 # run time (hh:mm:ss) 
#SBATCH -A Siegel-Group             # Allocation name to charge job against
#####################################################################

module purge
module load intel/19.1.1 impi/19.0.9
module load cuda/11.3 cudnn/8.2.1

#####################################################################

#source /work/09037/meohskim/vista/.mace_env/bin/activate

#export LD_LIBRARY_PATH=/work/09037/meohskim/vista/.mace_env/lib/python3.11/site-packages/torch/lib:$LD_LIBRARY_PATH
ibrun /corral/utexas/Siegel-Group/MACE_lammps/lammps/build2/lmp -in input.lammps
