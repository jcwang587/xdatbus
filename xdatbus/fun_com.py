import os
import shutil
import pandas as pd
import numpy as np
from ase.io import read
from ase import Atoms


def com_drift(xyz_path, frame_start=0, frame_end=None, save_csv=True, timestep=1):
    """
    Calculate the center of mass (COM) drift velocity for a xyz file.

    Parameters
    ----------
    xyz_path : str
        Path to the XYZ file.
    frame_start : int
        The first frame to consider.
    frame_end : int
        The last frame to consider. If None, considers all frames.
    save_csv : bool
        Whether to save the COM to a csv file.
    timestep : int
        The time difference between each frame, in appropriate time units. Default is 1.

    Returns
    -------
    np.ndarray
        The COM drift velocity, represented as a 3-element numpy array.
    """

    print("Loading the XYZ file ...")
    frames = read(xyz_path, index=":")

    if frame_end is None:
        frame_end = len(frames)

    com_list = []

    for frame in frames[frame_start:frame_end]:
        com_list.append(frame.get_center_of_mass())

    # save to csv file
    if save_csv:
        print("Saving the COM to a csv file ...")
        com_df = pd.DataFrame(com_list, columns=["x", "y", "z"])
        com_df.to_csv(xyz_path[:-4] + "_com.csv", index=False)

    # calculate the drift of the COM (last COM - first COM)
    drift = np.array(com_list[-1]) - np.array(com_list[0])

    # calculate the drift velocity
    drift_velocity = drift / ((frame_end - frame_start) * timestep)

    return drift, drift_velocity


def com_contcar(poscar_path, contcar_path, del_inter=False):
    """
    Correct the CONTCAR file by adding the COM drift to the coordinates of the CONTCAR file.
    The COM drift is calculated by fcom01_drift().

    Parameters
    ----------
    poscar_path : str
        Path to the POSCAR path.
    contcar_path : str
        Path to the CONTCAR file.
    del_inter : bool
        Delete the intermediate files created by this function.
    """

    # copy the CONTCAR file to a temporary file
    shutil.copy(contcar_path, "CONTCAR")
    shutil.copy(poscar_path, "POSCAR")

    # calculate the COM drift
    struct_poscar = read("POSCAR")
    struct_contcar = read("CONTCAR")
    com_drift = struct_contcar.get_center_of_mass() - struct_poscar.get_center_of_mass()

    # correct the CONTCAR file
    struct_contcar_corrected = Atoms(
        struct_contcar.get_chemical_symbols(),
        positions=struct_contcar.get_positions() - com_drift,
        cell=struct_contcar.get_cell(),
        pbc=True,
    )
    struct_contcar_corrected.write("CONTCAR_corrected")

    # print the COM for POSCAR, CONTCAR, and CONTCAR_corrected
    print("COM for POSCAR: {}".format(struct_poscar.get_center_of_mass()))
    print("COM for CONTCAR: {}".format(struct_contcar.get_center_of_mass()))
    print(
        "COM for CONTCAR_corrected: {}".format(
            struct_contcar_corrected.get_center_of_mass()
        )
    )

    # print the COM drift
    print("COM drift: {}".format(com_drift))

    # copy the corrected CONTCAR file to the aimd_path
    shutil.copy("CONTCAR_corrected", contcar_path.replace("CONTCAR", "CCONTCAR"))
    print("CCONTCAR file is copied to", contcar_path.replace("CONTCAR", "CCONTCAR"))

    # delete the intermediate files
    if del_inter:
        os.remove("CONTCAR")
        os.remove("CONTCAR_corrected")
        os.remove("POSCAR")
        print("Intermediate files are deleted.")
