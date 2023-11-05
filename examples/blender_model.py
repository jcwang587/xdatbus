import molecularnodes as mn
import bpy
import os
from xdatbus import pos2bpdb, realize_instances, clear_scene, apply_modifiers_to_mesh, render_image, rm_bond, yaml_gen, apply_yaml

current_dir = os.getcwd()
poscar_path = os.path.join(current_dir, '../tests/data/poscar/llto.poscar')
pdb_path = os.path.join(current_dir, 'llto.pdb')
pos2bpdb(poscar_path, pdb_path)

rm_bond('llto.pdb', "LI", "TI", "llto_rm_bond.pdb")
rm_bond("llto_rm_bond.pdb", "LA", "TI", "llto_rm_bond.pdb")
rm_bond("llto_rm_bond.pdb", "LA", "O", "llto_rm_bond.pdb")
rm_bond("llto_rm_bond.pdb", "LA", "LA", "llto_rm_bond.pdb")
rm_bond("llto_rm_bond.pdb", "LA", "LI", "llto_rm_bond.pdb")

# Set render engine to CYCLES and device to GPU
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = "GPU"

# Clear existing mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Load the molecule
clear_scene()
mol = mn.load.molecule_local("llto_rm_bond.pdb", default_style='ball_and_stick')
mol.rotation_euler = (0, 3.14 / 2, 0)
mol.select_set(True)
bpy.ops.view3d.camera_to_view_selected()

apply_yaml(mol, (255, 255, 255))

# Realize instances
realize_instances(mol)

# Export the scene to a blender file
output_blend_path = os.path.join(current_dir, 'output.blend')
bpy.ops.wm.save_as_mainfile(filepath=output_blend_path)

# Apply modifiers if the object is a mesh
apply_modifiers_to_mesh(mol)
#
# Render and save the image
# render_image_path = os.path.join(current_dir, 'render.png')  # Define the path for the output image
# render_image(output_path=render_image_path)  # Call the render function with the path
#
# Export the scene to an FBX file
output_fbx_path = os.path.join(current_dir, 'output.fbx')
bpy.ops.export_scene.fbx(filepath=output_fbx_path,
                         use_selection=True,
                         path_mode='COPY')
#
# # generate yaml file
# yaml_gen('config_template.yaml')
