#!/bin/bash
echo "Process ID : $$"

# Get the name of the current conda environment and directory
current_env=$(conda info --envs | grep ' \*' | awk '{print $1}')
current_dir=$(pwd)

echo "Current Environment: $current_env"
echo "Current Directory: $current_dir"

# Check if the 'plumed' package is installed in the current Conda environment
if conda list | grep -q "^plumed "; then
    echo "The 'plumed' package is installed in the current environment."
else
    echo "The 'plumed' package is not installed in the current environment."
    exit 1
fi

echo "Began running plumed!"

# Create a clean results folder
results_dir="${current_dir}/fes"
if [ ! -d "$results_dir" ]; then
    mkdir "$results_dir"
else
    find "$results_dir" -mindepth 1 -delete
fi

# Use arguments from the Python script
MIN="$1"
MAX="$2"
BIN="$3"

# Define HILLS file and output file
HILLS_FILE="${current_dir}/HILLS"
OUTFILE="${results_dir}/fes/fes_bias.dat"

# Validate HILLS file exists
if [ ! -f "$HILLS_FILE" ]; then
    echo "HILLS file not found: $HILLS_FILE"
    exit 1
fi

# Run Plumed with the given arguments
plumed sum_hills --hills "$HILLS_FILE" --outfile "$OUTFILE" --min "$MIN" --max "$MAX" --bin "$BIN"
