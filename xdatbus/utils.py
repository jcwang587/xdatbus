import os
import shutil
import numpy as np
from copy import deepcopy
from ase.io import read


def read_lat_vec(xdatcar_dir):
    """Read the lattice vectors from the first image of the XDATCAR file."""
    xdatcar = read(xdatcar_dir, format='vasp-xdatcar')
    lat_vec = np.array(xdatcar.get_cell())
    return lat_vec


def unwrap_pbc_dis(coord_1, coord_2, box_length):
    displacement = coord_2 - coord_1
    nearest_int = round(displacement / box_length)
    return displacement - nearest_int * box_length


def update_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)
