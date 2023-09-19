import os
import shutil
from ase.io import read
from ase import Atoms


def fcom03_contcar(poscar_path, contcar_path, del_inter=False):
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
    shutil.copy(contcar_path, 'CONTCAR')
    shutil.copy(poscar_path, 'POSCAR')

    # calculate the COM drift
    struct_poscar = read('POSCAR')
    struct_contcar = read('CONTCAR')
    com_drift = struct_contcar.get_center_of_mass() - struct_poscar.get_center_of_mass()

    # correct the CONTCAR file
    struct_contcar_corrected = Atoms(struct_contcar.get_chemical_symbols(),
                                     positions=struct_contcar.get_positions() - com_drift,
                                     cell=struct_contcar.get_cell(),
                                     pbc=True)
    struct_contcar_corrected.write('CONTCAR_corrected')

    # print the COM for POSCAR, CONTCAR, and CONTCAR_corrected
    print('COM for POSCAR: {}'.format(struct_poscar.get_center_of_mass()))
    print('COM for CONTCAR: {}'.format(struct_contcar.get_center_of_mass()))
    print('COM for CONTCAR_corrected: {}'.format(struct_contcar_corrected.get_center_of_mass()))

    # print the COM drift
    print('COM drift: {}'.format(com_drift))

    # copy the corrected CONTCAR file to the aimd_path
    shutil.copy('CONTCAR_corrected', contcar_path.replace('CONTCAR', 'CCONTCAR'))
    print('CCONTCAR file is copied to', contcar_path.replace('CONTCAR', 'CCONTCAR'))

    # delete the intermediate files
    if del_inter:
        os.remove('CONTCAR')
        os.remove('CONTCAR_corrected')
        os.remove('POSCAR')
        print('Intermediate files are deleted.')
