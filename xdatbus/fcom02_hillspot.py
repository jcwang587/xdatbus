import os
import shutil
import pandas as pd
from pymatgen.io.vasp.outputs import Xdatcar
from .fcom01_drift import fcom01_drift


def fcom02_hillspot(aimd_path, xyz_path='XDATBUS_unwrapped.xyz', freq=100, delete_intermediate_files=True):
    """
    Correct the HILLSPOT file by adding the COM drift to the first column of the HILLSPOT file.
    The COM drift is calculated by fcom01_drift().

    Parameters
    ----------
    aimd_path : str
        Path to the AIMD directory which contains the HILLSPOT and PENALTYPOT files.
    xyz_path : str
        Path to the unwrapped XYZ file.
    freq : int
        Frequency of the frames to update CV in Metadynamics.
    delete_intermediate_files : bool
        Delete the intermediate files created by this function.
    """
    com_drift = []
    total_frame = len(Xdatcar(aimd_path + 'XDATCAR').structures)
    for i in range(freq, total_frame+1, freq):
        com_drift.append(fcom01_drift(xyz_path, frame_start=0, frame_end=i, save_csv=False))
        print('COM drift for frames 0 to {} is {}'.format(i, com_drift[-1]))

    # correct the HILLS file
    # copy the HILLS file to the same directory as the XDATCAR file
    shutil.copy(aimd_path + 'HILLSPOT', 'HILLSPOT')
    shutil.copy(aimd_path + 'PENALTYPOT', 'PENALTYPOT')

    # read the files into dataframes
    hillspot_df = pd.read_csv('HILLSPOT', delimiter="\s+", header=None, names=['cv', 'height', 'sigma'])
    penaltypot_df = pd.read_csv('PENALTYPOT', delimiter="\s+", header=None, names=['cv', 'height', 'sigma'])

    mask = ~hillspot_df.isin(penaltypot_df).all(1)
    diff_df = hillspot_df[mask]

    # create a new diff_df with the corrected values by copying the original diff_df and replacing the first row
    diff_df_corrected = diff_df.copy()
    for i in range(len(com_drift)):
        diff_df_corrected.iloc[i]['cv'] += com_drift[i][2]

    # append the corrected diff_df to the original penaltypot_df
    penaltypot_df_corrected = pd.concat([penaltypot_df, diff_df_corrected])

    # Round dataframe to 5 decimal places
    penaltypot_df_corrected = penaltypot_df_corrected.round(5)

    # Convert DataFrame to string with a custom format and write it to a file
    with open('HILLSPOT_100K', 'w') as f:
        for row in penaltypot_df_corrected.itertuples(index=False, name=None):
            f.write("   {:.5f}   {:.5f}   {:.5f}\n".format(*row))

    # delete the intermediate files
    if delete_intermediate_files:
        os.remove('HILLSPOT')
        os.remove('PENALTYPOT')
