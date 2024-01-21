#!/bin/bash
echo "Process ID : $$"

# Save the process ID to a variable
process_id=$$

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

# Create a results folder with the process ID
results_dir="${current_dir}/fes_${process_id}"
if [ ! -d "$results_dir" ]; then
    mkdir "$results_dir"
else
    find "$results_dir" -mindepth 1 -delete
fi

# Parsing arguments passed to the script
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --min) MIN="$2"; shift ;;
        --max) MAX="$2"; shift ;;
        --bin) BIN="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Define HILLS file and output file
HILLS_FILE="${current_dir}/HILLS"
OUTFILE="${results_dir}/fes_bias.dat" # Fixed path to the outfile

# Validate HILLS file exists
if [ ! -f "$HILLS_FILE" ]; then
    echo "HILLS file not found: $HILLS_FILE"
    exit 1
fi

# Run Plumed with the given arguments
plumed sum_hills --hills "$HILLS_FILE" --outfile "$OUTFILE" --min "$MIN" --max "$MAX" --bin "$BIN"

# Print the command
echo "plumed sum_hills --hills $HILLS_FILE --outfile $OUTFILE --min $MIN --max $MAX --bin $BIN" --mintozero
