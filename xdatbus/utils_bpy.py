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