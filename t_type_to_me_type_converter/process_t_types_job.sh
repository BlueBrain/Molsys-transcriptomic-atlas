#!/bin/bash

#SBATCH --account=proj72 # PUT YOUR PROJ HERE
#SBATCH --job-name=convert_t_type_nrrds_to_me_type_nrrds    # Job name
#SBATCH --array=0-628                  # Job array range 
#SBATCH --output=./logs/batch_%A_%a.out     # Output file
#SBATCH --error=./logs/batch_%A_%a.err      # Error file
#SBATCH --time=24:00:00              # Time limit
#SBATCH --mem=0                    # Memory per job
#SBATCH --constraint=uc2
#SBATCH --partition=prod

# Load Python module
module load unstable
source ../myvenv/bin/activate

# Define paths
PATH_TO_T_TYPES_NRRDS="/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/results/density_calculations/scaled_nrrd_CCFv3a"
BATCH_SIZE=8  # Maximum number of T-types per job

# Dynamically calculate total T-types and batch size
TOTAL_T_TYPES=$(ls $PATH_TO_T_TYPES_NRRDS/*.nrrd | wc -l)  # Total T-types
NUM_BATCHES=$(( (TOTAL_T_TYPES + BATCH_SIZE - 1) / BATCH_SIZE ))  # Total number of batches

# Validate job array bounds
if [ $SLURM_ARRAY_TASK_ID -ge $NUM_BATCHES ]; then
  echo "No T-types to process for task ID $SLURM_ARRAY_TASK_ID."
  exit 0
fi

# Calculate start and end indices for this job
START=$((SLURM_ARRAY_TASK_ID * BATCH_SIZE))
END=$((START + BATCH_SIZE - 1))
if [ $END -ge $TOTAL_T_TYPES ]; then
  END=$((TOTAL_T_TYPES - 1))  # Adjust for the last batch
fi

# Ensure there is at least one T-type to process
if [ $START -gt $END ]; then
  echo "No T-types to process for task ID $SLURM_ARRAY_TASK_ID."
  exit 0
fi

# Run the Python script
echo "Processing T-types from index $START to $END..."
python convert_t_type_nrrds_to_me_type_nrrds.py --start $START --end $END --workers 4
