from xdatbus import set_color
import molecularnodes as mn

mol = mn.load.molecule_local("llto_rm_bond.pdb", default_style='ball_and_stick')

set_color(mol, (255, 255, 255))
