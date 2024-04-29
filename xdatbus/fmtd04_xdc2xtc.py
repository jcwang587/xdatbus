from ase.io import read, write
from MDAnalysis import Universe
from MDAnalysis.coordinates.XTC import XTCWriter


def xdc2xtc(xdc_path):
    """
    Convert a VASP XDATCAR file to an XTC trajectory file.

    Parameters
    ----------
    xdc_path : str
        Path to the XDATCAR file
    """
    # Load XDATCAR using ASE and write to a temporary XYZ file
    xdatcar = read(xdc_path, format="vasp-xdatcar", index=":")
    temp_xyz_path = xdc_path + ".xyz"
    xtc_path = xdc_path + ".xtc"

    with open(temp_xyz_path, 'w') as file:
        write(file, xdatcar, format='xyz')

    # close the file
    file.close()

    # Initialize MDAnalysis Universe
    u = Universe(temp_xyz_path)

    # Write out the XTC file
    with XTCWriter(xtc_path, n_atoms=u.atoms.n_atoms) as w:
        for ts in u.trajectory:
            print(f"Writing frame {ts.frame}")
            w.write(u.atoms)



