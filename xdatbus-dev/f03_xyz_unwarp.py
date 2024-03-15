import os
import numpy as np
from pymatgen.io.xyz import XYZ
from xdatbus.utils import unwrap_pbc_dis


def xyz_unwrap(xyz_path, lattice):
    """
    Unwrap the coordinates in the xyz file. The unwrapped coordinates will be written to a new xyz file.

        Parameters
        ----------
        xyz_path : str
            Input path of the xyz file
        lattice : list
            Lattice vectors of the system
    """
    xyz = XYZ.from_file(xyz_path)
    # initialize an empty list to store unwrapped fractional coordinates
    unwrapped_coords = []

    # Initialize a variable to store the previously unwrapped coordinates
    previous_unwrapped_coords = xyz.all_molecules[0].cart_coords

    unwrapped_coords.append(
        previous_unwrapped_coords.copy()
    )  # Store the first set of coordinates

    for i in range(1, len(xyz.all_molecules)):  # Start from the second frame
        if (i + 1) % 1000 == 0:
            print("Processing frame " + str(i + 1) + " ...")

        # initialize an empty array for the current structure's unwrapped coordinates
        current_unwrapped_coords = np.zeros_like(xyz.all_molecules[i].cart_coords)

        for j in range(len(xyz.all_molecules[i].cart_coords)):
            for k in range(3):
                # update the current coordinates
                current_wrapped_coords = xyz.all_molecules[i].cart_coords[j][k]
                displacement = unwrap_pbc_dis(
                    previous_unwrapped_coords[j][k], current_wrapped_coords, lattice[k]
                )
                current_unwrapped_coords[j][k] = (
                    previous_unwrapped_coords[j][k] + displacement
                )

        # update the previous unwrapped coordinates for next frame
        previous_unwrapped_coords = current_unwrapped_coords.copy()

        # append the current structure's unwrapped coordinates to the list
        unwrapped_coords.append(current_unwrapped_coords)

    # open the output xyz file
    output_filename = os.path.basename(xyz_path).replace(".xyz", "_unwrapped.xyz")
    output_path = os.path.join(os.path.dirname(xyz_path), output_filename)
    with open(output_path, "w") as xyz_file:
        for i, coords in enumerate(unwrapped_coords):
            # write the current structure to the xyz file
            xyz_file.write(str(len(xyz.all_molecules[i].species)) + "\n\n")
            for atom, coord in zip(xyz.all_molecules[i].species, coords):
                xyz_file.write("{} {:.8f} {:.8f} {:.8f}\n".format(atom.symbol, *coord))

    print("xdatbus-func: xyz_unwrap: Done!")
