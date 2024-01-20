#!/bin/bash
echo "Process ID : $$"

# Get the name of the current conda environment and directory
current_env=$(conda info --envs | grep '*' | awk '{print $1}')
current_dir=$(pwd)
in_dir="$current_dir/in"
res_dir="$current_dir/res"

# Check if the current environment is "my_plumed"
if [ "$current_env" != "my_plumed" ]; then
    # Activate "my_plumed" environment
    eval "$(conda shell.bash hook)"
    conda activate my_plumed
    echo "Activated 'my_plumed' environment."
else
    echo "The 'my_plumed' environment is already active."
fi

echo "Began running plumed!"

# Create a clean results folder
if [ ! -d "res" ]; then
    mkdir "res"
else
    find "res" -mindepth 1 -delete
fi

# Run Plumed
cd "$in_dir"
plumed sum_hills --hills HILLS --outfile ../res/fes_bias.dat --mintozero --min 0 --max 11.636 --bin 100

# Post process
ln -sf ~/softwares/plumed/bin/save_bias_fes.plt "$res_dir"
cd "$res_dir"
gnuplot save_bias_fes.plt
