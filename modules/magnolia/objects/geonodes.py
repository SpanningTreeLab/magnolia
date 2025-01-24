from typing import cast, Optional, Union

import bpy

from .objects import ObjectArg, resolve_object


def apply_geonodes(
    arg: ObjectArg,
    name: Optional[str] = None,
    nodes: Union[bpy.types.GeometryNodeTree, str, None] = "NEW",
) -> bpy.types.NodesModifier:
    """
    Apply Geometry Nodes modifier to an object.

    Arguments:

    - `arg`: Object onto which to apply geometry nodes.

    Optional arguments:

    - `name`: Name for the geometry nodes modifier
    - `nodes`: Node group to use for the modiifer. Defaults to "NEW", which will create a new node
      group. If set to `None`, no node group will be set.
    """
    obj = resolve_object(arg)

    # Create Geometry Nodes modifier
    modifier = cast(
        bpy.types.NodesModifier, obj.modifiers.new(name or "Geometry Nodes", "NODES")
    )

    # Create a new node group
    if nodes == "NEW":
        group = create_geonodes_group(name)
        modifier.node_group = group
    elif nodes is not None:
        modifier.node_group = nodes  # pyright: ignore

    return modifier


def create_geonodes_group(name: Optional[str] = None) -> bpy.types.GeometryNodeTree:
    """
    Creates a new Geometry Nodes node tree.
    """
    group = cast(
        bpy.types.GeometryNodeTree,
        bpy.data.node_groups.new(
            name or "Geometry Nodes", "GeometryNodeTree"  # pyright: ignore
        ),
    )

    # Create input node and add geometry socket
    input_node = group.nodes.new("NodeGroupInput")
    input_node.location = (0, 0)
    group.interface.new_socket(
        "Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
    )

    # Create output node and add geometry socket
    output_node = group.nodes.new("NodeGroupOutput")
    output_node.location = (400, 0)
    group.interface.new_socket(
        "Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
    )

    # Link geometry input to geometry output
    group.links.new(
        input_node.outputs["Geometry"],
        output_node.inputs["Geometry"],
    )

    return group
