import molecularnodes as mn
import bpy
import os
from xdatbus import pos2bpdb, realize_instances


def clear_scene():
    # Clear mesh objects
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.object.select_by_type(type="MESH")
    bpy.ops.object.delete()

    # Clear light objects
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.object.select_by_type(type="LIGHT")
    bpy.ops.object.delete()

    # Clear geometry node groups
    for node in bpy.data.node_groups:
        if node.type == "GEOMETRY":
            bpy.data.node_groups.remove(node)


def render_image(engine='eevee', x=1000, y=500, output_path='render.png'):  # Added output_path parameter
    # setup render engine
    if engine == "eevee":
        bpy.context.scene.render.engine = "BLENDER_EEVEE"
    elif engine == "cycles":
        bpy.context.scene.render.engine = "CYCLES"
        try:
            bpy.context.scene.cycles.device = "GPU"
        except:
            print("GPU Rendering not available")

    # Render
    bpy.context.scene.render.resolution_x = x
    bpy.context.scene.render.resolution_y = y
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.filepath = output_path  # Use the output_path
    bpy.ops.render.render(write_still=True)


def apply_modifiers_to_mesh(obj):
    # Ensure we are operating on the correct object
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Check if the object is a mesh and apply modifiers accordingly
    if obj.type == 'MESH':
        for modifier in obj.modifiers:
            print(f"Applying modifier: {modifier.name}")
            try:
                bpy.ops.object.modifier_apply(modifier=modifier.name)
            except Exception as e:
                print(f"Failed to apply modifier {modifier.name}: {e}")
    else:
        print(f"Cannot apply modifiers to non-mesh object: {obj.name}")


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
clear_scene()
mol = mn.load.molecule_local(pdb_path, default_style='ball_and_stick')
mol.rotation_euler = (0, 3.14 / 2, 0)
mol.select_set(True)
bpy.ops.view3d.camera_to_view_selected()

# Realize instances
realize_instances(mol)

# Apply modifiers if the object is a mesh
apply_modifiers_to_mesh(mol)

# Render and save the image
render_image_path = os.path.join(current_dir, 'render.png')  # Define the path for the output image
render_image(output_path=render_image_path)  # Call the render function with the path

# Export the scene to an FBX file
output_fbx_path = os.path.join(current_dir, 'output.fbx')
bpy.ops.export_scene.fbx(filepath=output_fbx_path,
                         use_selection=True,
                         path_mode='COPY')
