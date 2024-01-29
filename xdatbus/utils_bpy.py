import importlib.resources as pkg_resources
from ase.io import read
from ase.data import atomic_numbers

try:
    import bpy

    BPY_AVAILABLE = True
except ImportError:
    bpy = None
    BPY_AVAILABLE = False

try:
    import biotite.structure.io.pdb as pdb

    PDB_AVAILABLE = True
except ImportError:
    pdb = None
    PDB_AVAILABLE = False

try:
    import molecularnodes as mn

    MN_AVAILABLE = True
except ImportError:
    mn = None
    MN_AVAILABLE = False

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    yaml = None
    YAML_AVAILABLE = False

global bonded_element


def realize_instances(obj, bond_radius):
    """
    Realize instances of the given object. This function requires bpy.

        Parameters
        ----------
        obj : bpy.types.Object
            The object to realize instances of
        bond_radius : float
            The radius of the bonds
    """
    if not BPY_AVAILABLE:
        raise ImportError(
            "The function `realize_instances` requires bpy. Please install bpy to use this function."
        )

    if obj.modifiers:
        # Find the GeometryNodes modifier
        geo_node_mod = next((mod for mod in obj.modifiers if mod.type == "NODES"), None)
        if geo_node_mod:
            # Get the node group (node tree) used by this modifier
            node_group = geo_node_mod.node_group
            nodes = node_group.nodes

            # Check if 'Realize Instances' node already exists
            realize_node = next(
                (
                    node
                    for node in nodes
                    if node.bl_idname == "GeometryNodeRealizeInstances"
                ),
                None,
            )

            if not realize_node:
                # Create a new 'Realize Instances' node
                realize_node = nodes.new(type="GeometryNodeRealizeInstances")

            # Find the Group Output node
            group_output = next(
                (node for node in nodes if node.bl_idname == "NodeGroupOutput"), None
            )
            if group_output is None:
                print("Group Output node not found.")
                return

            # Store the sockets before removing the links
            stored_sockets = [
                (link.from_socket, link.to_socket)
                for link in node_group.links
                if link.to_node == group_output
            ]

            # Disconnect all inputs of the Group Output node
            for from_socket, to_socket in stored_sockets:
                node_group.links.remove(
                    next(
                        (
                            link
                            for link in node_group.links
                            if link.from_socket == from_socket
                            and link.to_socket == to_socket
                        ),
                        None,
                    )
                )

            # Add a join geometry node
            join_node = nodes.new(type="GeometryNodeJoinGeometry")

            # Get the MN_style_sticks node from the blend template
            style_sticks_node = get_template_node("MN_style_sticks", nodes)
            style_sticks_node.inputs["Radius"].default_value = bond_radius
            style_sticks_node.inputs["Resolution"].default_value = 20
            style_sticks_node.inputs["Material"].default_value = bpy.data.materials[
                "MN_atomic_material"
            ]

            # Connect the Group Input node to the Style Sticks node
            node_group.links.new(
                style_sticks_node.outputs["Sticks"], join_node.inputs["Geometry"]
            )
            node_group.links.new(join_node.outputs[0], realize_node.inputs[0])
            node_group.links.new(realize_node.outputs[0], group_output.inputs[0])

            # # Trigger update
            # geo_node_mod.node_group = None
            # geo_node_mod.node_group = node_group
            #
            # # Update scene
            # bpy.context.view_layer.update()


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
    geo_node_mod = next((mod for mod in obj.modifiers if mod.type == "NODES"), None)

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


def get_template_node(node_name, nodes):
    """
    Get a node from a template blend file.

        Parameters
        ----------
        node_name : str
            The name of the node to get.
        nodes : bpy.types.NodeTree.nodes
            The nodes from the node tree to add the node to.

        Returns
        -------
        node : bpy.types.Node
            The node from the template blend file.
    """
    blend_path = str(pkg_resources.path("xdatbus.resources", "node_data.blend"))
    bpy.ops.wm.append(filename=node_name, directory=blend_path + "\\NodeTree\\")
    node_group = bpy.data.node_groups[node_name]
    node = nodes.new(type="GeometryNodeGroup")
    node.node_tree = node_group

    return node


def set_color4element(obj, atomic_number, color, atomic_scale, bonded, bonded_count=0):
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
        atomic_scale : float
            The size of the atoms.
        bonded : bool
            Whether the atoms are bonded.
        bonded_count : int
            The number of elements forming a bond.
    """

    # Get the Geometry Nodes modifier from the object
    geo_node_mod = next((mod for mod in obj.modifiers if mod.type == "NODES"), None)

    if geo_node_mod:
        # Get the node group (node tree) used by this modifier
        node_group = geo_node_mod.node_group
        nodes = node_group.nodes

        # Find necessary nodes
        group_input = next(
            (node for node in nodes if node.bl_idname == "NodeGroupInput"), None
        )
        join_node = next(
            (node for node in nodes if node.bl_idname == "GeometryNodeJoinGeometry"),
            None,
        )
        style_sticks_node = next(
            (
                node
                for node in nodes
                if node.bl_idname == "GeometryNodeGroup"
                and node.node_tree.name == "MN_style_sticks"
            ),
            None,
        )

        # Set color for atoms and link the nodes
        atom_color_set_node = get_template_node("MN_color_set", nodes)
        r, g, b, alpha = color
        atom_color_set_node.inputs["Color"].default_value = (
            r / 255,
            g / 255,
            b / 255,
            alpha,
        )
        node_group.links.new(
            group_input.outputs["Geometry"], atom_color_set_node.inputs["Atoms"]
        )

        # Set the Eevee render engine
        style_atoms_node = get_template_node("MN_style_atoms", nodes)
        style_atoms_node.inputs["[ ] Cycles / [x] Eevee "].default_value = True
        style_atoms_node.inputs["Scale Radii"].default_value = atomic_scale
        style_atoms_node.inputs[4].default_value = 5
        style_atoms_node.inputs["Material"].default_value = bpy.data.materials[
            "MN_atomic_material"
        ]
        node_group.links.new(
            atom_color_set_node.outputs["Atoms"], style_atoms_node.inputs["Atoms"]
        )
        node_group.links.new(
            style_atoms_node.outputs["Geometry"], join_node.inputs["Geometry"]
        )

        # Get the MN_select_atomic_number node from the blend template
        select_atomic_number_node = get_template_node("MN_select_atomic_number", nodes)
        select_atomic_number_node.inputs["atomic_number"].default_value = atomic_number
        node_group.links.new(
            select_atomic_number_node.outputs["Selection"],
            atom_color_set_node.inputs["Selection"],
        )
        node_group.links.new(
            select_atomic_number_node.outputs["Selection"],
            style_atoms_node.inputs["Selection"],
        )

        # Get the MN_color_attribute_random node from the blend template
        if bonded:
            bond_color_set_node = get_template_node("MN_color_set", nodes)
            bond_color_set_node.name = "MN_color_set_bond_{}".format(bonded_count)
            bond_color_set_node.inputs["Color"].default_value = (
                r / 255,
                g / 255,
                b / 255,
                alpha,
            )

            bond_select_atomic_number_node = get_template_node(
                "MN_select_atomic_number", nodes
            )
            bond_select_atomic_number_node.inputs["atomic_number"].default_value = (
                atomic_number
            )
            node_group.links.new(
                bond_select_atomic_number_node.outputs["Selection"],
                bond_color_set_node.inputs["Selection"],
            )

            if bonded_count == 0:
                node_group.links.new(
                    group_input.outputs["Geometry"], bond_color_set_node.inputs["Atoms"]
                )
                node_group.links.new(
                    bond_color_set_node.outputs["Atoms"],
                    style_sticks_node.inputs["Atoms"],
                )
            else:
                # find the node with the highest bond_count
                bond_color_set_node_prev = next(
                    (
                        node
                        for node in nodes
                        if node.name == "MN_color_set_bond_{}".format(bonded_count - 1)
                    ),
                    None,
                )
                node_group.links.new(
                    bond_color_set_node_prev.outputs["Atoms"],
                    bond_color_set_node.inputs["Atoms"],
                )
                node_group.links.new(
                    bond_color_set_node.outputs["Atoms"],
                    style_sticks_node.inputs["Atoms"],
                )

            bonded_count += 1

    return bonded_count


def apply_yaml(obj, yaml_path):
    """
    Set the color of the given object. This function requires bpy and molecularnodes.

    Parameters
    ----------
    obj : bpy.types.Object
        The object to set the color of
    yaml_path : str
        The path to the YAML file to use
    """
    global bonded_element
    bonded_element = 0

    if not BPY_AVAILABLE or not MN_AVAILABLE:
        raise ImportError(
            "The function `apply_yaml` requires bpy and molecularnodes. Please install bpy and "
            "molecularnodes to use this function."
        )

    # Load the YAML file and extract only the elements data
    elements_data, bond_radius = yaml_loader(yaml_path)

    # Prepare the object for editing
    realize_instances(obj, bond_radius)
    remove_nodes(
        obj,
        [
            "MN_color_common",
            "MN_color_attribute_random",
            "MN_color_set",
            "MN_style_ball_and_stick",
        ],
    )

    # Set the properties for each element
    for element, attributes in elements_data.items():
        atomic_number = int(attributes["atomic_number"])
        color = tuple(attributes["color"])
        atomic_scale = float(attributes["atomic_scale"])
        bonded = bool(attributes["bonded"])
        bonded_element = set_color4element(
            obj, atomic_number, color, atomic_scale, bonded, bonded_element
        )


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
        raise ImportError(
            "The function `clear_scene` requires bpy. Please install bpy to use this function."
        )

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


def render_image(engine="eevee", x=1000, y=500, output_path="render.png"):
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
        raise ImportError(
            "The function `render_image` requires bpy. Please install bpy to use this function."
        )

    # setup render engine
    if engine == "eevee":
        bpy.context.scene.render.engine = "BLENDER_EEVEE"
    elif engine == "cycles":
        bpy.context.scene.render.engine = "CYCLES"
        if "GPU" in bpy.context.scene.cycles.available_devices:
            bpy.context.scene.cycles.device = "GPU"
        else:
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
        raise ImportError(
            "The function `apply_modifiers_to_mesh` requires bpy. Please install bpy to use this "
            "function."
        )

    # Ensure we are operating on the correct object
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Check if the object is a mesh and apply modifiers accordingly
    if obj.type == "MESH":
        for modifier in obj.modifiers:
            print(f"Applying modifier: {modifier.name}")
            try:
                bpy.ops.object.modifier_apply(modifier=modifier.name)
            except Exception as e:
                print(f"Failed to apply modifier {modifier.name}: {e}")
    else:
        print(f"Cannot apply modifiers to non-mesh object: {obj.name}")


def yaml_gen(pdb_file_path):
    """
    This function generates a YAML file for the elements in the PDB file, with a common bond_radius.

    Parameters
    ----------
    pdb_file_path : str
        Input path of the PDB file
    """
    if not YAML_AVAILABLE:
        raise ImportError(
            "The function `yaml_gen` requires PyYAML. Please install PyYAML to use this function."
        )

    # Initialize a set to hold unique elements
    unique_elements = set()

    # Read the PDB file and extract unique elements
    with open(pdb_file_path, "r") as file:
        for line in file:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                element_symbol = line[76:78].strip()  # Extract the element symbol
                formatted_symbol = element_symbol.capitalize()
                unique_elements.add(formatted_symbol)

    # Create a dictionary for elements with default color, size scale, and atomic number
    elements_dict = {
        "elements": {
            element: {
                "atomic_number": atomic_numbers[element],
                "color": [0, 0, 0, 1],  # RGBA for black with full opacity
                "atomic_scale": 0.4,
                "bonded": True,
            }
            for element in unique_elements
        },
        "bond_radius": 0.25,  # Common bond radius for all elements
    }

    color_path = str(pkg_resources.path("xdatbus.resources", "color_data.yaml"))

    # Find if the element is in the color_data.yaml file and update the color
    with open(color_path, "r") as file:
        color_data = yaml.safe_load(file)
        for element, attributes in elements_dict["elements"].items():
            if element in color_data["elements"]:
                elements_dict["elements"][element]["color"] = color_data["elements"][
                    element
                ]["color"]

    # Extract the PDB ID from the file name for naming the YAML file
    pdb_id = pdb_file_path.split("/")[-1].split(".")[0]

    # Generate YAML string from dictionary
    yaml_str = yaml.safe_dump(elements_dict, sort_keys=True, default_flow_style=False)

    # Write YAML string to file
    yaml_file_path = f"{pdb_id}_style.yaml"
    with open(yaml_file_path, "w") as file:
        file.write(yaml_str)

    print(f"YAML file '{yaml_file_path}' has been created.")


def yaml_loader(yaml_path):
    """
    This function loads a YAML file and returns element data and bond radius.

    Parameters
    ----------
    yaml_path : str
        Input path of the YAML file

    Returns
    -------
    tuple
        A tuple containing a dictionary of elements with their properties and the common bond radius.
    """
    if not YAML_AVAILABLE:
        raise ImportError(
            "The function `yaml_loader` requires yaml. Please install yaml to use this function."
        )

    with open(yaml_path, "r") as file:
        data = yaml.safe_load(file)

    elements_data = {}
    # Extract the bond_radius from the root level of the data
    bond_radius = data.get("bond_radius")

    # Process each element's attributes
    for element, attributes in data.get("elements", {}).items():
        atomic_number = int(attributes["atomic_number"])
        color = tuple(attributes["color"])
        atomic_scale = float(attributes["atomic_scale"])
        bonded = bool(attributes["bonded"])
        elements_data[element] = {
            "atomic_number": atomic_number,
            "color": color,
            "atomic_scale": atomic_scale,
            "bonded": bonded,
        }

    return elements_data, bond_radius
