import os
import re
import shutil
import numpy as np
from ase.io import read


def read_lat_vec(xdatcar_dir):
    """Read the lattice vectors from the first image of the XDATCAR file."""
    xdatcar = read(xdatcar_dir, format="vasp-xdatcar")
    lat_vec = np.array(xdatcar.get_cell())
    return lat_vec


def unwrap_pbc_dis(coord_1, coord_2, box_length):
    """
    Unwrap the distance between two coordinates.

        Parameters
        ----------
        coord_1 : ndarray
            The first coordinate
        coord_2 : ndarray
            The second coordinate
        box_length :
            The length of the box

        Returns
        -------
        float
            The unwrapped distance between the two coordinates
    """
    displacement = coord_2 - coord_1
    nearest_int = round(displacement / box_length)
    return displacement - nearest_int * box_length


def update_folder(folder):
    """
    Delete the folder and create a new one.

        Parameters
        ----------
        folder : str
            The path of the folder
    """
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)


def remove_file(file_path):
    """
    Delete the file.

        Parameters
        ----------
        file_path : str
            The path of the file
    """
    if os.path.exists(file_path):
        os.remove(file_path)


# Define a function to skip lines starting with #!
def skip_comments(file):
    with open(file, "r") as f:
        return [i for i, line in enumerate(f) if line.startswith("#!")]


def filter_files(files, pattern):
    pattern = re.compile(rf"{pattern}")
    return [file for file in files if pattern.search(file)]


def gauss_pot_1d(x: np.ndarray, x0: float, height: float, width: float) -> np.ndarray:
    """
    Calculate the Gaussian potential energy.

    Parameters:
    - x (np.ndarray): Array of positions at which to evaluate the potential.
    - x0 (float): The position of the potential minimum.
    - height (float): The height of the Gaussian potential.
    - width (float): The standard deviation (controls the width of the Gaussian).

    Returns:
    - np.ndarray: The potential energy at each position x.
    """
    en = height * np.exp(-((x - x0) ** 2) / (2.0 * width**2))
    return en


def gauss_pot_2d(
    x: np.ndarray, y: np.ndarray, x0: float, y0: float, height: float, width: float
) -> np.ndarray:
    """
    Calculate the Gaussian potential energy.

    Parameters:
    - x (np.ndarray): Array of x positions at which to evaluate the potential.
    - y (np.ndarray): Array of y positions at which to evaluate the potential.
    - x0 (float): The x position of the potential minimum.
    - y0 (float): The y position of the potential minimum.
    - height (float): The height of the Gaussian potential.
    - width (float): The standard deviation (controls the width of the Gaussian).

    Returns:
    - np.ndarray: The potential energy at each position (x, y).
    """
    en = height * np.exp(-((x - x0) ** 2 + (y - y0) ** 2) / (2.0 * width**2))
    return en


def gauss_pot_3d(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    x0: float,
    y0: float,
    z0: float,
    height: float,
    width: float,
) -> np.ndarray:
    """
    Calculate the Gaussian potential energy.

    Parameters:
    - x (np.ndarray): Array of x positions at which to evaluate the potential.
    - y (np.ndarray): Array of y positions at which to evaluate the potential.
    - z (np.ndarray): Array of z positions at which to evaluate the potential.
    - x0 (float): The x position of the potential minimum.
    - y0 (float): The y position of the potential minimum.
    - z0 (float): The z position of the potential minimum.
    - height (float): The height of the Gaussian potential.
    - width (float): The standard deviation (controls the width of the Gaussian).

    Returns:
    - np.ndarray: The potential energy at each position (x, y, z).
    """
    en = height * np.exp(
        -((x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2) / (2.0 * width**2)
    )
    return en
