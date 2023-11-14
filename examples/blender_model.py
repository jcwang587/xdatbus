import os
import bpy
import time
import molecularnodes as mn
from xdatbus.fbld01_pos2bpdb import pos2bpdb
from xdatbus.fbld02_rm_bond import rm_bond
from xdatbus.utils_bpy import clear_scene, apply_modifiers_to_mesh, apply_yaml, yaml_gen

current_dir = os.getcwd()
poscar_path = os.path.join(current_dir, '../tests/data/poscar/llto.poscar')
pdb_path = os.path.join(current_dir, 'llto.pdb')
pos2bpdb(poscar_path, pdb_path)

rm_bond('llto.pdb', "LI", "TI", "llto_rm_bond.pdb")
rm_bond("llto_rm_bond.pdb", "LA", "TI", "llto_rm_bond.pdb")
rm_bond("llto_rm_bond.pdb", "LA", "O", "llto_rm_bond.pdb")
rm_bond("llto_rm_bond.pdb", "LA", "LA", "llto_rm_bond.pdb")
rm_bond("llto_rm_bond.pdb", "LA", "LI", "llto_rm_bond.pdb")

# Generate YAML file
# yaml_gen('llto_rm_bond.pdb')

# Start timer
start_time = time.time()

# Load the molecule and apply the style
clear_scene()
mol = mn.load.molecule_local("llto_rm_bond.pdb", default_style='ball_and_stick')
apply_yaml(mol, 'llto_rm_bond_style.yaml')

# Export the scene to a blender file
output_blend_path = os.path.join(current_dir, 'output.blend')
bpy.ops.wm.save_as_mainfile(filepath=output_blend_path)

# Apply modifiers if the object is a mesh
apply_modifiers_to_mesh(mol)

# Export the scene to an FBX file
output_fbx_path = os.path.join(current_dir, 'output.fbx')
bpy.ops.export_scene.fbx(filepath=output_fbx_path,
                         use_selection=True,
                         path_mode='COPY')

# End timer
end_time = time.time()

# Print the time taken
print("Time taken: {} seconds".format(end_time - start_time))

