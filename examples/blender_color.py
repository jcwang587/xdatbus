from xdatbus import apply_yaml
import molecularnodes as mn

mol = mn.load.molecule_local("llto_rm_bond.pdb", default_style='ball_and_stick')

apply_yaml(mol, (255, 255, 255))
