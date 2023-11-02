import os
import bpy
import molecularnodes as mn
from xdatbus import pos2bpdb

current_dir = os.getcwd()
poscar_path = os.path.join(current_dir, '../tests/data/poscar/llto.poscar')
pdb_path = os.path.join(current_dir, 'llto.pdb')
pos2bpdb(poscar_path, pdb_path)

# Set render engine to CYCLES and device to GPU
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = "GPU"

# Clear existing mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Load the molecule
obj = mn.load.molecule_local(pdb_path, default_style='ball_and_stick')

# Set the active object
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# If Molecular Nodes creates instances, make them real here
if hasattr(obj, 'instance_collection') and obj.instance_collection is not None:
    bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
    obj.select_set(True)  # Select only the object with instances
    bpy.ops.object.duplicates_make_real()  # Make instances real

# Apply all modifiers for the object
for modifier in obj.modifiers:
    bpy.ops.object.modifier_apply(modifier=modifier.name)

# Export the scene to an FBX file
output_fbx_path = os.path.join(current_dir, 'output.fbx')
bpy.ops.export_scene.fbx(filepath=output_fbx_path, use_selection=True)
