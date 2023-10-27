from ase.io import read
import pybel


def pos2bpdb(poscar_path, output_path):
    # Load the POSCAR file with ASE
    atoms = read(poscar_path)

    # Convert the ASE atoms object to an XYZ format (string)
    xyz_data = atoms.write('-',
                           format='xyz',
                           return_data=True)

    # Use Pybel to read the XYZ string
    mol = pybel.readstring('xyz', xyz_data)

    # Write the molecule to a PDB file
    mol.write('pdb', output_path, overwrite=True)



