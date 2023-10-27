from ase.io import read
from rdkit import Chem


def pos2bpdb(poscar_path, output_path):
    # Load the POSCAR file with ASE
    atoms = read(poscar_path)

    # Convert ASE atoms to RDKit molecule
    atomic_numbers = atoms.get_atomic_numbers()
    positions = atoms.get_positions()

    # Create an empty RWMol object
    rwmol = Chem.RWMol()

    for atomic_num, pos in zip(atomic_numbers, positions):
        atom = Chem.Atom(int(atomic_num))  # Explicitly convert to int
        rwmol.AddAtom(atom)

    # Add a conformer to the RWMol object
    conf = Chem.Conformer(len(atomic_numbers))
    for idx, pos in enumerate(positions):
        conf.SetAtomPosition(idx, tuple(pos))
    rwmol.AddConformer(conf)

    # Convert RWMol back to Mol
    mol = rwmol.GetMol()

    # Convert RDKit molecule to PDB format and save
    Chem.MolToPDBFile(mol, output_path)



