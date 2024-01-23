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
        --hills) HILLS="$2"; shift ;;
        --outfile) OUTFILE="$2"; shift ;;
        --min) MIN="$2"; shift ;;
        --max) MAX="$2"; shift ;;
        --bin) BIN="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Validate HILLS file exists
if [ ! -f "$HILLS" ]; then
    echo "HILLS file not found: $HILLS"
    exit 1
fi

# Copy the HILLS file to the results folder
cp "$HILLS" "$results_dir"/HILLS

# Run Plumed with the given arguments
plumed sum_hills \
    --hills "$HILLS" \
    --outfile "$results_dir"/"$OUTFILE" \
    --mintozero \
    --min "$MIN" \
    --max "$MAX" \
    --bin "$BIN" \
    > "$results_dir/stdout.$process_id" 2> "$results_dir/stderr.$process_id"

# Print the command
echo "plumed sum_hills --hills $HILLS --outfile $results_dir/$OUTFILE --mintozero --min $MIN --max $MAX --bin $BIN"
