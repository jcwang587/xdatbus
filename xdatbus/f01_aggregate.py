import os
import re
import shutil
from ase.io import read, write
from pymatgen.io.vasp.outputs import Xdatcar
from .utils import update_folder


def f01_aggregate(
        aimd_path,
        min_frames=1,
        delete_temp_files=True
):
    """
    Initialize a trajectory writer instance for *filename*.

        Parameters
        ----------
        aimd_path : str
            Output filename of the trajectory; the extension determines the format.
        min_frames : int (optional)
            Minimum number of frames in each XDATCAR file, which will be used to be appended to the trajectory
        delete_temp_files : bool (optional)
            If ``True``, the intermediate folders will be deleted
    """

    raw_list = os.listdir(aimd_path)
    raw_list_sort = sorted(raw_list, key=lambda x: int(re.findall(r'\d+', x)[0]))

    xdatcar_wrap = "./xdatcar_wrap"

    # Clear the directory
    update_folder(xdatcar_wrap)

    # Remove the XDATBUS and log files
    if os.path.exists("XDATBUS"):
        os.remove("XDATBUS")
    if os.path.exists("XDATBUS.log"):
        os.remove("XDATBUS.log")

    log_file = open("XDATBUS.log", "w")
    for xdatcar_raw in raw_list_sort:
        print("Wrapping " + xdatcar_raw + " ...")
        xdatcar = read(aimd_path + "/" + xdatcar_raw, format='vasp-xdatcar', index=':')
        print("Number of frames in " + xdatcar_raw + ": " + str(len(xdatcar)))
        if len(xdatcar) > min_frames:
            write(xdatcar_wrap + "/" + xdatcar_raw, format='vasp-xdatcar', images=xdatcar)
            log_file.write(xdatcar_raw + " " + str(len(xdatcar)) + "\n")
    log_file.close()

    # Get the number of files in wrap directory
    wrap_list = os.listdir(xdatcar_wrap)
    wrap_list_sort = sorted(wrap_list, key=lambda x: int(re.findall(r'\d+', x)[0]))

    # Combine the wrapped XDATCAR files into one XDATCAR file (XDATBUS) using pymatgen
    print("Combining XDATCAR files into one XDATCAR file ...")
    # Initialize the XDATCAR bus with the first XDATCAR file
    xdatbus = Xdatcar(xdatcar_wrap + "/" + wrap_list_sort[0])

    for xdatcar_wrap in wrap_list_sort[1:]:
        print("Appending " + xdatcar_wrap + " ...")
        xdatcar = Xdatcar(xdatcar_wrap + "/" + xdatcar_wrap)
        xdatbus.structures.extend(xdatcar.structures)
    xdatbus.write_file('XDATBUS')

    if delete_temp_files:
        shutil.rmtree(xdatcar_wrap)
        os.remove("XDATBUS.log")

    print("xdatbus-func: f01_aggregate: Done!")

