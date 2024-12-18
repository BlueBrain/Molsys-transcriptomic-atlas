#!/bin/bash -l

#SBATCH --job-name=density_to_nrrd
#SBATCH --account=proj84
#SBATCH --partition=prod
#SBATCH --constraint=cpu
#SBATCH --mem=0 
#SBATCH --time=9:00:00
#SBATCH --output=outputs/%A_%a.log
#SBATCH --error=error/stderr-%A_%a.log
#SBATCH --array=0-39%40

echo "Starting process: $(date)"
echo "The NRRD save folder must be emptied before running this script !" # > /dev/tty

#Check if the folder we save the files are empty: scaled_nrrd_CCFv3_0 / scaled_nrrd_CCFv3a / scaled_nrrd
root_folder=$(grep "^root_folder =" /gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/notebooks/scripts/density2_comp_nrrd_on_1node_scaled.py | awk -F"'" '{print $2}' | sed 's/$/nrrd\//')

if [ -z "$root_folder" ]; then
    echo "The NRRD save folder is empty. Python will generate new nrrd files."
else
    echo "The NRRD save folder is not empty! You may not generate new nrrd files!"
fi


###
#This code will run the same name .py file which processes csv files of cell type densities and 
#projects them into the CCF while creating nrrd files. 
###

echo "Loading Python: $(date +"%T.%3N")"

# Load Python environment
module unload python
#conda activate cell2loc
conda activate cellden

#Provide cycles (where to parse the data) which is passed on the the working node
nodes=( $(seq 1 30) )
celltype_batch="On Node${nodes[${SLURM_ARRAY_TASK_ID}]}"
echo $celltype_batch

# python /gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/notebooks/scripts/calc_av_jobarray_writegpfs.py "$celltype_batch"

exec python /gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/notebooks/scripts/density2_comp_nrrd_on_1node.py 
# exec python /gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/notebooks/scripts/density2_comp_nrrd_on_1node_scaled.py
 

# Print "Job's done" message to the log files
echo "All jobs are done: $(date)"