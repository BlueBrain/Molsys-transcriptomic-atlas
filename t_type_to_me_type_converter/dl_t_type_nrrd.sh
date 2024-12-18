# 1. Get the list of files from the remote server and save it locally
files=$(ssh yroussel@bbpv1.epfl.ch "ls /gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/results/density_calculations/scaled_nrrd_CCFv3a")

# 2. Sample 10 evenly spaced files from the list
sample_files=$(echo "$files" | awk 'NR % 450 == 1' | head -n 10)

# 3. Use scp to copy each selected file
for file in $sample_files; do
    scp yroussel@bbpv1.epfl.ch:/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/results/density_calculations/scaled_nrrd_CCFv3a/"$file" ./
done
