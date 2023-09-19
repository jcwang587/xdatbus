import os
import shutil
import MDAnalysis as MDa
from ase.io import read, write
from pymatgen.io.vasp.outputs import Xdatcar


def fm01_xdatcar2xtc(
        aimd_path,
        last_frame=False,
        xtc=False
):
    """
    Initialize a trajectory writer instance for *filename*.

        Parameters
        ----------
        aimd_path : str
            Output filename of the trajectory; the extension determines the
            format.
        last_frame : bool (optional)
            If ``True``, the trajectory will contain the last frame
        xtc : bool (optional)
            The number of atoms in the output trajectory; can be ommitted
            for single-frame writers.

    """

    # Define the path to the XDATCAR file
    file_list = os.listdir(aimd_path)
    run_list = [run for run in file_list if 'RUN' in run]
    # sort run_list by the number in the run name
    run_list.sort(key=lambda x: int(x[3:]))
    xdatcar_U1_N0_OV0_2000K = [aimd_path + "/" + run_list[i] + "/XDATCAR" for i in range(len(run_list))]
    xdatcar_U1_N0_OV0_2000K_latest = aimd_path + "/XDATCAR"

    local_xdatcar_files_raw = "./xdatcar_files_raw"
    local_xdatcar_files_wrap = "./xdatcar_files_wrap"

    # Clear the directory
    if os.path.exists(local_xdatcar_files_raw):
        shutil.rmtree(local_xdatcar_files_raw)
    os.mkdir(local_xdatcar_files_raw)
    if os.path.exists(local_xdatcar_files_wrap):
        shutil.rmtree(local_xdatcar_files_wrap)
    os.mkdir(local_xdatcar_files_wrap)

    # Copy the XDATCAR file to the current directory
    print("Copying XDATCAR files to the current directory ...")
    i = 0
    for i in range(len(xdatcar_U1_N0_OV0_2000K)):
        shutil.copy(xdatcar_U1_N0_OV0_2000K[i], "./xdatcar_files_raw/XDATCAR_" + str(i + 1))
    if last_frame:
        shutil.copy(xdatcar_U1_N0_OV0_2000K_latest, "./xdatcar_files_raw/XDATCAR_" + str(i + 2))

    # Extract the lattice vectors from the first image of the XDATCAR file
    a = Xdatcar("./xdatcar_files_raw/XDATCAR_1").structures[0].lattice.a
    b = Xdatcar("./xdatcar_files_raw/XDATCAR_1").structures[0].lattice.b
    c = Xdatcar("./xdatcar_files_raw/XDATCAR_1").structures[0].lattice.c

    # Get the number of AIMD runs
    if last_frame:
        mdrun = len(xdatcar_U1_N0_OV0_2000K) + 1
    else:
        mdrun = len(xdatcar_U1_N0_OV0_2000K)

    for i in range(mdrun):
        print("Wrapping XDATCAR_" + str(i + 1) + " ...")
        xdatcar = read("./xdatcar_files_raw/XDATCAR_" + str(i + 1), format='vasp-xdatcar', index=':')
        write("./xdatcar_files_wrap/XDATCAR_" + str(i + 1), format='vasp-xdatcar', images=xdatcar)

    # Combine the wrapped XDATCAR files into one XDATCAR file (XDATBUS) using pymatgen
    print("Combining XDATCAR files into one XDATCAR file ...")
    xdatbus = Xdatcar("./xdatcar_files_wrap/XDATCAR")

    for i in range(mdrun - 1):
        xdatbus.concatenate("./xdatcar_files_wrap/XDATCAR_" + str(i + 2))
        print("XDATCAR_" + str(i + 2) + " is concatenated.")
    xdatbus.write_file('XDATBUS')

    # Convert the XDATCAR file to xyz format
    print("Converting XDATCAR to xyz format ...")
    xdatbusxyz_ase = read('XDATBUS', format='vasp-xdatcar', index=':')
    write('XDATBUS.xyz', xdatbusxyz_ase, format='xyz')
    u = MDa.Universe('XDATBUS.xyz')

    if xtc:
        # Write out the XTC file
        with MDa.Writer("trajectory.xtc", u.atoms.n_atoms) as w:
            for ts in u.trajectory:
                print("Writing frame %d" % ts.frame)
                w.write(u.atoms)

    print("Done.")
