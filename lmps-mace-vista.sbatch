#!/bin/bash
#“#SBATCH” directives that convey submission options:

##### The name of the job
#SBATCH -J lmps-mace                # Job name
#SBATCH -o output.o%j               # output and error file name (%j expands to jobID)
#SBATCH -e output.e%j               # Name of stderr error file
#SBATCH -p gh                       # queue (partition) 
#SBATCH -N 1                        # number of nodes requested
#SBATCH -n 1                        # total number of tasks to run in parallel
#SBATCH --cpus-per-task=16          # Use 16 CPU cores for data loading
#SBATCH -t 8:00:00                  # run time (hh:mm:ss) 
#SBATCH -A Siegel-Group             # Allocation name to charge job against
#####################################################################

module purge
module load gcc/13.2.0
module load cuda/12.8
module load openmpi/5.0.5
module load python3/3.11.8

#####################################################################

source /work/09037/meohskim/vista/.mace_env/bin/activate

export LD_LIBRARY_PATH=/work/09037/meohskim/vista/.mace_env/lib/python3.11/site-packages/torch/lib:$LD_LIBRARY_PATH
ibrun /home1/09037/meohskim/lammps/build-hopper/bin/lmp -k on g 1 -sf kk -pk kokkos neigh half -in input.lammps
