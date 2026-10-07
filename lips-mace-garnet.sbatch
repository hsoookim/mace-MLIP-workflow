#!/bin/bash
#SBATCH -J MACE-lmp                 # Job name
#SBATCH -o output.o%j               # output and error file name (%j expands to jobID)
#SBATCH -e output.e%j               # Name of stderr error file
#SBATCH -N 1                        # number of nodes requested
#SBATCH -n 2                        # total number of tasks to run in parallel
#SBATCH --cpus-per-task=16          # CPU cores for data loading
#SBATCH --mem=16G
#SBATCH -t 200:00:00                # run time (hh:mm:ss) 

#####################################################################

module purge
module load intel/2025.3.0 impi/2021.14 mpi/2021.14 mkl

#####################################################################

mpirun -n 1 /opt/apps/MACE_lammps/lammps/build/lmp -in input.lammps -log log.lammps
