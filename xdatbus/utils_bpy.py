import importlib.resources as pkg_resources

try:
    import bpy

    BPY_AVAILABLE = True
except ImportError:
    bpy = None
    BPY_AVAILABLE = False

try:
    import molecularnodes as mn

    MN_AVAILABLE = True
except ImportError:
    mn = None
    MN_AVAILABLE = False


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


def remove_nodes(obj, node_names):
    """
    Remove nodes with given names from the object's node tree.

        Parameters
        ----------
        obj : bpy.types.Object
            The object from which to remove nodes.
        node_names : list of str
            The names of the nodes to remove.
    """
    # Get the Geometry Nodes modifier from the object
    geo_node_mod = next((mod for mod in obj.modifiers if mod.type == 'NODES'), None)

    if geo_node_mod:
        # Get the node group (node tree) used by this modifier
        node_group = geo_node_mod.node_group
        nodes = node_group.nodes

        # Loop through all provided node names and remove them
        for node_name in node_names:
            node_to_remove = nodes.get(node_name)
            if node_to_remove:
                # Use nodes.remove() to delete the node
                nodes.remove(node_to_remove)
                print(f"Removed node: {node_name}")
            else:
                print(f"Node {node_name} not found.")


def get_template_node(template_path, node_name, nodes):
    """
    Get a node from a template blend file.

        Parameters
        ----------
        template_path : str
            The path to the template blend file.
        node_name : str
            The name of the node to get.
        nodes : bpy.types.NodeTree.nodes
            The nodes from the node tree to add the node to.

        Returns
        -------
        node : bpy.types.Node
            The node from the template blend file.
    """
    # Get the template blend file
    blend_path = pkg_resources.path('xdatbus.resources', template_path)

    # Get the node from the blend template
    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        data_to.node_groups = [node_name]

    # Put the node in the node tree
    node_group = data_to.node_groups[0]

    node = nodes.new(type='GeometryNodeGroup')
    node.node_tree = node_group

    return node


def set_color4element(obj, atomic_number, color):
    """
    Add a custom node and connect it to the specified input of the target node.

        Parameters
        ----------
        obj : bpy.types.Object
            The object with the Geometry Nodes modifier whose node tree we're editing.
        atomic_number : int
            The atomic number of the element to set the color of.
        color : tuple
            The color to set the node to.
    """

    # Get the Geometry Nodes modifier from the object
    geo_node_mod = next((mod for mod in obj.modifiers if mod.type == 'NODES'), None)

    if geo_node_mod:
        # Get the node group (node tree) used by this modifier
        node_group = geo_node_mod.node_group
        nodes = node_group.nodes

        # Get the MN_color_set node from the blend template
        color_set_node = get_template_node('resources/h2o.blend', 'MN_color_set', nodes)

        # Rename the node to include the atomic number
        color_set_node.name = f'MN_color_set_{atomic_number}'
        color_set_node.label = f'MN_color_set_{atomic_number}'

        # Find the Group Input node
        group_input = next((node for node in nodes if node.bl_idname == 'NodeGroupInput'), None)
        if group_input is None:
            print("Group Input node not found.")
            return

        # Connect the Group Input node to the Color Set node
        node_group.links.new(group_input.outputs[0], color_set_node.inputs['Atoms'])
        node_group.links.new(color_set_node.outputs['Atoms'],
                             node_group.nodes['MN_style_ball_and_stick'].inputs['Atoms'])

        # Get the MN_color_atomic_number node from the blend template
        atomic_number_node = get_template_node('resources/h2o.blend', 'MN_color_atomic_number', nodes)

        # Set the atomic number and color
        atomic_number_node.inputs['atomic_number'].default_value = atomic_number
        atomic_number_node.inputs['Color'].default_value = color

        # Rename the node to include the atomic number
        atomic_number_node.name = f'MN_color_atomic_number_{atomic_number}'
        atomic_number_node.label = f'MN_color_atomic_number_{atomic_number}'

        # link the node to the color_set_node
        node_group.links.new(atomic_number_node.outputs['Color'], color_set_node.inputs['Color'])

        # Update the node tree to reflect changes
        node_group.update_tag()


def apply_yaml(obj, color):
    """
    Set the color of the given object. This function requires bpy and molecularnodes.

        Parameters
        ----------
        obj : bpy.types.Object
            The object to set the color of
        color : tuple
            The color to set the object to
    """
    if not BPY_AVAILABLE or not MN_AVAILABLE:
        raise ImportError("The function `set_color` requires bpy and molecularnodes. Please install bpy and "
                          "molecularnodes to use this function.")

    # Find the GeometryNodes modifier
    geo_node_mod = next((mod for mod in obj.modifiers if mod.type == 'NODES'), None)
    if geo_node_mod:
        # Get the node group (node tree) used by this modifier
        node_group = geo_node_mod.node_group
        nodes = node_group.nodes

        for node in nodes:
            print(node.name, node.bl_idname)

        remove_nodes(obj, ['MN_color_common', 'MN_color_attribute_random', 'MN_color_set'])

        set_color4element(obj, 3, (0.155483, 0.204112, 0.8, 1))
        set_color4element(obj, 8, (0.8, 0.0, 0.0, 1))


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
