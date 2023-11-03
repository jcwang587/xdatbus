import numpy as np
from rdkit import Chem
from ase.io import read
from ase.data import covalent_radii
from biotite.structure.io import load_structure


def pos2bpdb(poscar_path, output_path):
    """
    Convert the POSCAR file to a PDB file which can be read by biotite.

        Parameters
        ----------
        poscar_path : str
            Input path of the POSCAR file
        output_path : str
            Output path of the PDB file
    """
    # Load the POSCAR file with ASE
    atoms = read(poscar_path)

    # Convert ASE atoms to RDKit molecule
    atomic_numbers = atoms.get_atomic_numbers()
    positions = atoms.get_positions()

    # Create an empty RWMol object for editing
    rwmol = Chem.RWMol()

    for atomic_num, pos in zip(atomic_numbers, positions):
        atom = Chem.Atom(int(atomic_num))
        rwmol.AddAtom(atom)

    # Add a conformer to the RWMol object
    conf = Chem.Conformer(len(atomic_numbers))
    for idx, pos in enumerate(positions):
        conf.SetAtomPosition(idx, tuple(pos))
    rwmol.AddConformer(conf)

    # Use distance to infer bonds
    for i in range(len(atomic_numbers)):
        for j in range(i + 1, len(atomic_numbers)):
            dist = np.linalg.norm(positions[i] - positions[j])
            # Sum of covalent radii as a simple check
            if dist < covalent_radii[atomic_numbers[i]] + covalent_radii[atomic_numbers[j]]:
                rwmol.AddBond(i, j, Chem.BondType.SINGLE)  # Assuming single bond for simplicity

    # Convert RDKit molecule to PDB format and save
    mol = rwmol.GetMol()
    Chem.MolToPDBFile(mol, output_path)

    # Check if the output file is readable by biotite
    try:
        load_structure(output_path)
    except ValueError:
        print("Output file is not readable by biotite")
    else:
        print("Output file is readable by biotite")
