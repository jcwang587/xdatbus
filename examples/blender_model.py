import molecularnodes as mn
import bpy
import os
from xdatbus import pos2bpdb


def realize_instances(obj):
    if obj.modifiers:
        # Find the GeometryNodes modifier
        geo_node_mod = next((mod for mod in obj.modifiers if mod.type == 'NODES'), None)
        if geo_node_mod:
            # Get the node group (node tree) used by this modifier
            node_group = geo_node_mod.node_group
            nodes = node_group.nodes

            # Check if 'Realize Instances' node already exists
            realize_node = next((node for node in nodes if node.bl_idname == 'GeometryNodeRealizeInstances'), None)

            if not realize_node:
                # Create a new 'Realize Instances' node
                realize_node = nodes.new(type='GeometryNodeRealizeInstances')

            # Find the Group Output node
            group_output = next((node for node in nodes if node.bl_idname == 'NodeGroupOutput'), None)
            if group_output is None:
                print("Group Output node not found.")
                return

            # Store the sockets before removing the links
            stored_sockets = [(link.from_socket, link.to_socket) for link in node_group.links if
                              link.to_node == group_output]

            # Disconnect all inputs of the Group Output node
            for from_socket, to_socket in stored_sockets:
                node_group.links.remove(next((link for link in node_group.links if
                                              link.from_socket == from_socket and link.to_socket == to_socket), None))

            # Connect the Realize Instances node to the Group Output node
            node_group.links.new(realize_node.outputs[0], group_output.inputs[0])

            # Ensure the Realize Instances node gets inputs from the previous node in the tree
            if stored_sockets:
                # Connect the stored 'from socket' to the input of the 'Realize Instances' node
                node_group.links.new(stored_sockets[0][0], realize_node.inputs[0])

            # Trigger update
            geo_node_mod.node_group = None
            geo_node_mod.node_group = node_group

            # Update scene
            bpy.context.view_layer.update()


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
