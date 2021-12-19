#!/bin/bash
#
# Simple SLURM script for submitting multiple serial
# jobs (e.g. parametric studies) using a script wrapper
# to launch the jobs.
#
# To use, build the launcher executable and your
# serial application(s) and place them in your WORKDIR
# directory.  Then, edit the CONTROL_FILE to specify
# each executable per process.
#-------------------------------------------------------
#-------------------------------------------------------
#
#         <------ Setup Parameters ------>
#
#SBATCH -J strain
#SBATCH -N 128 -n 256
#SBATCH -p flex
#SBATCH -o strain_%j.out
#SBATCH -e strain_%j.err
#SBATCH -t 1:00:00
#SBATCH --mail-user=ericchang347@gmail.com
#SBATCH --mail-type=all
#SBATCH -A Swallowing
#------------------------------------------------------

module load launcher
export LAUNCHER_PPN=3

export LAUNCHER_JOB_FILE=/scratch1/08503/ehc547/strain.job
export LAUNCHER_WORKDIR=/scratch1/08503/ehc547/strain

export LAUNCHER_PLUGIN_DIR=$LAUNCHER_DIR/plugins
export LAUNCHER_RMI=SLURM

$LAUNCHER_DIR/paramrun