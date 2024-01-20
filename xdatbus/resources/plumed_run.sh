#!/bin/bash
echo "Process ID : $$"

# Get the name of the current conda environment and directory
current_env=$(conda info --envs | grep '*' | awk '{print $1}')
current_dir=$(pwd)

# Check if the 'plumed' package is installed in the current Conda environment
if conda list | grep -q "^plumed "; then
    echo "The 'plumed' package is installed in the current environment."
else
    echo "The 'plumed' package is not installed in the current environment."
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
