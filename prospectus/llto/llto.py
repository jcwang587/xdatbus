import os
from xdatbus.fbld01_pos2bpdb import pos2bpdb
from xdatbus.fbld02_rm_bond import rm_bond


def rm_bond_llto(pdb):
    rm_bond(pdb, "LI", "TI", pdb)
    rm_bond(pdb, "LI", "O", pdb)
    rm_bond(pdb, "LA", "TI", pdb)
    rm_bond(pdb, "LA", "O", pdb)
    rm_bond(pdb, "LA", "LA", pdb)
    rm_bond(pdb, "LA", "LI", pdb)


current_dir = os.getcwd()
poscar_path = os.path.join(current_dir, 'llto_n0_ov0.poscar')
pdb_path = os.path.join(current_dir, 'llto_n0_ov0.pdb')
pos2bpdb(poscar_path, pdb_path)
rm_bond_llto(pdb_path)

poscar_path = os.path.join(current_dir, 'mid.poscar')
pdb_path = os.path.join(current_dir, 'mid.pdb')
pos2bpdb(poscar_path, pdb_path)
rm_bond_llto(pdb_path)

poscar_path = os.path.join(current_dir, 'la_rich.poscar')
pdb_path = os.path.join(current_dir, 'la_rich.pdb')
pos2bpdb(poscar_path, pdb_path)
rm_bond_llto(pdb_path)
