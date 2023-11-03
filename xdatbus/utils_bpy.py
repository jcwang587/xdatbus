try:
    import bpy

    BPY_AVAILABLE = True
except ImportError:
    bpy = None
    BPY_AVAILABLE = False


def realize_instances(obj):
    """
    Realize instances of the given object. This function requires bpy.

        Parameters
        ----------
        obj : bpy.types.Object
            The object to realize instances of
    """
    if not BPY_AVAILABLE:
        raise ImportError("The function `realize_instances` requires bpy. Please install bpy to use this function.")

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


def clear_scene(mesh=True, lights=True, geometry_nodes=True):
    """
    Clear the scene of all objects. This function requires bpy.

        Parameters
        ----------
        mesh : bool
            Clear mesh objects
        lights : bool
            Clear light objects
        geometry_nodes : bool
            Clear geometry node groups
    """
    if not BPY_AVAILABLE:
        raise ImportError("The function `clear_scene` requires bpy. Please install bpy to use this function.")

    if mesh:
        bpy.ops.object.select_all(action="DESELECT")
        bpy.ops.object.select_by_type(type="MESH")
        bpy.ops.object.delete()

    if lights:
        bpy.ops.object.select_all(action="DESELECT")
        bpy.ops.object.select_by_type(type="LIGHT")
        bpy.ops.object.delete()

    if geometry_nodes:
        for node in bpy.data.node_groups:
            if node.type == "GEOMETRY":
                bpy.data.node_groups.remove(node)


def render_image(engine='eevee', x=1000, y=500, output_path='render.png'):
    """
    Render an image. This function requires bpy.

        Parameters
        ----------
        engine : str
            The render engine to use. Either 'eevee' or 'cycles'
        x : int
            The x resolution of the image
        y : int
            The y resolution of the image
        output_path : str
            The path to save the image to
    """
    if not BPY_AVAILABLE:
        raise ImportError("The function `render_image` requires bpy. Please install bpy to use this function.")

    # setup render engine
    if engine == "eevee":
        bpy.context.scene.render.engine = "BLENDER_EEVEE"
    elif engine == "cycles":
        bpy.context.scene.render.engine = "CYCLES"
        try:
            bpy.context.scene.cycles.device = "GPU"
        except:
            bpy.context.scene.cycles.device = "CPU"

    # Render
    bpy.context.scene.render.resolution_x = x
    bpy.context.scene.render.resolution_y = y
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.filepath = output_path

    bpy.ops.render.render(write_still=True)


def apply_modifiers_to_mesh(obj):
    """
    Apply modifiers to the given object. This function requires bpy.

        Parameters
        ----------
        obj : bpy.types.Object
            The object to apply modifiers to
    """
    if not BPY_AVAILABLE:
        raise ImportError("The function `apply_modifiers_to_mesh` requires bpy. Please install bpy to use this "
                          "function.")

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