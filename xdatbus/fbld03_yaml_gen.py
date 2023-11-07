import biotite.structure.io.pdb as pdb
import yaml


def yaml_gen(pdb_file_path):
    # Create a PDBFile object
    pdb_file = pdb.PDBFile.read(pdb_file_path)

    # Convert PDB file to an AtomArray
    atom_array = pdb.get_structure(pdb_file)[0]  # [0] to get the first model if multiple models are present

    # Extract the PDB ID from the file name for naming the YAML file
    pdb_id = pdb_file_path.split('/')[-1].split('.')[0]

    # Get unique elements from the atom array
    unique_elements = set(atom_array.element.astype(str))  # Convert elements to Python strings

    # Create a dictionary for elements with default color and size scale
    elements_dict = {
        str(element): {  # Ensure that element is a Python string
            'color': [0, 0, 0, 1],  # RGBA for black with full opacity as a list
            'size_scale': 0.8
        }
        for element in unique_elements
    }

    # Generate YAML string from dictionary
    # Use default_flow_style=False to output a traditional YAML format
    yaml_str = yaml.safe_dump(elements_dict, sort_keys=True, default_flow_style=False)

    # Write YAML string to file
    with open(f'{pdb_id}_style.yaml', 'w') as file:
        file.write(yaml_str)

    print(f"YAML file '{pdb_id}_style.yaml' has been created.")
