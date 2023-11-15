try:
    import biotite
    BIOTITE_AVAILABLE = True
except ImportError:
    biotite = None
    BIOTITE_AVAILABLE = False


def rm_bond(pdb_file_path, element1, element2, output_file_path):
    """
    This function removes CONECT records involving bonds between element1 and element2.

        Parameters
        ----------
        pdb_file_path : str
            Input path of the PDB file
        element1 : str
            The first element in the bond to remove
        element2 : str
            The second element in the bond to remove
        output_file_path : str
            Output path of the PDB file
    """
    if not BIOTITE_AVAILABLE:
        raise ImportError("The function `rm_bond` requires biotite. Please install biotite to use this function.")

    # Load the PDB file into a list of lines
    with open(pdb_file_path, 'r') as file:
        lines = file.readlines()

    # Create a dictionary that maps atom serial numbers to element types
    atom_elements = {}
    for line in lines:
        if line.startswith("ATOM") or line.startswith("HETATM"):
            atom_serial_number = int(line[6:11].strip())
            atom_element = line[76:78].strip()
            atom_elements[atom_serial_number] = atom_element

    # Create a list to hold the new lines
    new_lines = []

    # Iterate through the lines and process the CONECT records
    for line in lines:
        if line.startswith("CONECT"):
            # Parse the connected atoms
            connected_atoms = [int(x) for x in line[6:].split()]
            if not connected_atoms:
                continue
            atom_serial_number = connected_atoms[0]
            connected_serial_numbers = connected_atoms[1:]

            # Iterate through connected serial numbers and remove only the specified bonds
            connected_serial_numbers = [
                s for s in connected_serial_numbers
                if not (
                        (atom_elements.get(atom_serial_number) == element1 and atom_elements.get(s) == element2) or
                        (atom_elements.get(atom_serial_number) == element2 and atom_elements.get(s) == element1)
                )
            ]

            # If there are no connected serial numbers left, skip adding this line
            if not connected_serial_numbers:
                continue

            # Construct a new CONECT line with the remaining connections
            new_conect_line = f"CONECT{atom_serial_number:>5}" + "".join(
                f"{s:>5}" for s in connected_serial_numbers) + "\n"
            new_lines.append(new_conect_line)
            continue

        # Add the line to the new_lines list if it's not a CONECT line
        new_lines.append(line)

    # Write the new PDB content to the output file
    with open(output_file_path, 'w') as file:
        file.writelines(new_lines)



