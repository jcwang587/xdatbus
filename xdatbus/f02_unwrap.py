import numpy as np
from pymatgen.io.vasp.outputs import Xdatcar
from .utils import unwrap_pbc_dis


def f02_unwrap(xdatcar_path):
    print('Loading the XDATCAR file ...')
    xdatcar = Xdatcar(xdatcar_path)
    # initialize an empty list to store unwrapped fractional coordinates
    unwrapped_coords = []

    # Initialize a variable to store the previously unwrapped coordinates
    previous_unwrapped_coords = xdatcar.structures[0].frac_coords
    unwrapped_coords.append(previous_unwrapped_coords.copy())  # Store the first set of coordinates

    for i in range(1, len(xdatcar.structures)):  # Start from the second frame
        print('Processing frame ' + str(i + 1) + ' ...')

        # initialize an empty array for the current structure's unwrapped coordinates
        current_unwrapped_coords = np.zeros_like(xdatcar.structures[i].frac_coords)

        for j in range(len(xdatcar.structures[i].frac_coords)):
            for k in range(3):
                # update the current coordinates
                displacement = unwrap_pbc_dis(previous_unwrapped_coords[j][k],
                                              xdatcar.structures[i].frac_coords[j][k], 1)
                current_unwrapped_coords[j][k] = previous_unwrapped_coords[j][k] + displacement

        # update the previous unwrapped coordinates for next frame
        previous_unwrapped_coords = current_unwrapped_coords.copy()

        # append the current structure's unwrapped coordinates to the list
        unwrapped_coords.append(current_unwrapped_coords)

    # open the output xyz file
    with open(xdatcar_path + '_unwrapped.xyz', 'w') as xyz_file:
        for i, coords in enumerate(unwrapped_coords):
            # write the current structure to the xyz file
            xyz_file.write(str(len(xdatcar.structures[i].species)) + '\n\n')
            for atom, coord in zip(xdatcar.structures[i].species, coords):
                xyz_file.write('{} {:.8f} {:.8f} {:.8f}\n'.format(atom.symbol, *coord))

    print('Finished writing the unwrapped coordinates to the xyz file.')
