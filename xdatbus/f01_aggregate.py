import os
import shutil
from ase.io import read, write
from pymatgen.io.vasp.outputs import Xdatcar


def f01_aggregate(
        aimd_path,
        load_pre_xdatcar=True,
        load_last_xdatcar=False,
        min_frames=1,
        delete_intermediate_folders=True
):
    """
    Initialize a trajectory writer instance for *filename*.

        Parameters
        ----------
        aimd_path : str
            Output filename of the trajectory; the extension determines the format.
        load_pre_xdatcar : bool (optional)
            If ``True``, the trajectory will contain the previous frames (before the current run)
        load_last_xdatcar : bool (optional)
            If ``True``, the trajectory will contain the last frame
        min_frames : int (optional)
            Minimum number of frames in each XDATCAR_01 file, which will be used to be appended to the trajectory
        delete_intermediate_folders : bool (optional)
            If ``True``, the intermediate folders will be deleted
    """

    # Define the path to the XDATCAR_01 file
    remote_file_list = os.listdir(aimd_path)
    run_list = [run for run in remote_file_list if 'RUN' in run]
    # sort run_list by the number in the run name
    run_list.sort(key=lambda x: int(x[3:]))
    xdatcar_path_list = [aimd_path + "/" + run_list[i] + "/XDATCAR" for i in range(len(run_list))]
    xdatcar_path_last = aimd_path + "/XDATCAR"

    local_xdatcar_files_raw = "./xdatcar_files_raw"
    local_xdatcar_files_wrap = "./xdatcar_files_wrap"

    # Clear the directory
    if os.path.exists(local_xdatcar_files_raw):
        shutil.rmtree(local_xdatcar_files_raw)
    os.mkdir(local_xdatcar_files_raw)
    if os.path.exists(local_xdatcar_files_wrap):
        shutil.rmtree(local_xdatcar_files_wrap)
    os.mkdir(local_xdatcar_files_wrap)

    # Remove the XDATBUS and log files
    if os.path.exists("XDATBUS"):
        os.remove("XDATBUS")
    if os.path.exists("XDATBUS.log"):
        os.remove("XDATBUS.log")

    # Copy the XDATCAR file to the current directory
    print("Copying XDATCAR files to the current directory ...")
    i = 0
    if load_pre_xdatcar:
        for i in range(len(xdatcar_path_list)):
            shutil.copy(xdatcar_path_list[i], "./xdatcar_files_raw/" + "XDATCAR_" + str(i + 1).zfill(5))
    if load_last_xdatcar:
        if load_pre_xdatcar:
            shutil.copy(xdatcar_path_last, "./xdatcar_files_raw/" + "XDATCAR_" + str(i + 2).zfill(5))
        else:
            shutil.copy(xdatcar_path_last, "./xdatcar_files_raw/" + "XDATCAR_" + str(i + 1).zfill(5))

    # Get the number of files in wrap directory
    raw_list = os.listdir(local_xdatcar_files_raw)
    raw_list.sort()

    log_file = open("XDATBUS.log", "w")
    for xdatcar_wrap in raw_list:
        print("Wrapping " + xdatcar_wrap + " ...")
        xdatcar = read("./xdatcar_files_raw/" + xdatcar_wrap, format='vasp-xdatcar', index=':')
        print("Number of frames in " + xdatcar_wrap + ": " + str(len(xdatcar)))
        if len(xdatcar) > min_frames:
            write("./xdatcar_files_wrap/" + xdatcar_wrap, format='vasp-xdatcar', images=xdatcar)
            log_file.write(xdatcar_wrap + " " + str(len(xdatcar)) + "\n")
    log_file.close()

    # Get the number of files in wrap directory
    wrap_list = os.listdir(local_xdatcar_files_wrap)
    wrap_list.sort()

    # Combine the wrapped XDATCAR files into one XDATCAR file (XDATBUS) using pymatgen
    print("Combining XDATCAR files into one XDATCAR file ...")
    # Initialize the XDATCAR bus with the first XDATCAR file
    xdatbus = Xdatcar("./xdatcar_files_wrap/" + wrap_list[0])

    for xdatcar_wrap in wrap_list[1:]:
        print("Appending " + xdatcar_wrap + " ...")
        xdatcar = Xdatcar("./xdatcar_files_wrap/" + xdatcar_wrap)
        xdatbus.structures.extend(xdatcar.structures)
    xdatbus.write_file('XDATBUS')

    if delete_intermediate_folders:
        shutil.rmtree(local_xdatcar_files_raw)
        shutil.rmtree(local_xdatcar_files_wrap)

    print("Done.")
