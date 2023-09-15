from ase.io import read
import pandas as pd
import numpy as np


def fcom01_drift(xyz_path, frame_start=0, frame_end=None, save_csv=True, timestep=1):
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

    print('Loading the XYZ file ...')
    frames = read(xyz_path, index=':')

    if frame_end is None:
        frame_end = len(frames)

    com_list = []

    for frame in frames[frame_start:frame_end]:
        com_list.append(frame.get_center_of_mass())

    # save to csv file
    if save_csv:
        print('Saving the COM to a csv file ...')
        com_df = pd.DataFrame(com_list, columns=['x', 'y', 'z'])
        com_df.to_csv(xyz_path[:-4] + '_com.csv', index=False)

    # calculate the drift of the COM (last COM - first COM)
    drift = np.array(com_list[-1]) - np.array(com_list[0])

    # calculate the drift velocity
    drift_velocity = drift / ((frame_end - frame_start) * timestep)

    return drift, drift_velocity
