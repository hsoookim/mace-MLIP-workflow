#!/bin/bash
#“#SBATCH” directives that convey submission options:

##### The name of the job
#SBATCH -J model                    # Job name
#SBATCH -o output.o%j               # output and error file name (%j expands to jobID)
#SBATCH -e output.e%j               # Name of stderr error file
#SBATCH -p gh                       # queue (partition) 
#SBATCH -N 1                        # number of nodes requested
#SBATCH -n 1                        # total number of tasks to run in parallel
#SBATCH --cpus-per-task=16          # Use 16 CPU cores for data loading
#SBATCH -t 48:00:00                 # run time (hh:mm:ss) 
#SBATCH -A Siegel-Group             # Allocation name to charge job against
#####################################################################

module purge
module load gcc/15.1.0
module load cuda/12.8
module load python3/3.11.8

#####################################################################

source /work/09037/meohskim/vista/.mace_env/bin/activate

mace_run_train --config config_L.yml

#convert to lammps-pt
python -m mace.cli.create_lammps_model mace_mo/mace_mo_stagetwo.model --dtype float64
~                                                                                                              
~                                                                                                              
~                                                                                                              
~                                                                                                              
~                                                                                                              
~                                                                                                              
~    
