#!/bin/bash
echo "Process ID : $$"

# Get the name of the current conda environment and directory
current_env=$(conda info --envs | grep '*' | awk '{print $1}')
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
if [ ! -d "fes" ]; then
    mkdir "fes"
else
    find "fes" -mindepth 1 -delete
fi

# Use arguments from the Python script
MINTOZERO="$1"
MIN="$2"
MAX="$3"
BIN="$4"

# Validate arguments (example for HILLS_FILE)
if [ ! -f "$HILLS_FILE" ]; then
    echo "HILLS file not found: $HILLS_FILE"
    exit 1
fi

# Run Plumed with the given arguments
plumed sum_hills --hills HILLS --outfile ./fes/fes_bias.dat --mintozero "$MINTOZERO" --min "$MIN" --max "$MAX" --bin "$BIN"

