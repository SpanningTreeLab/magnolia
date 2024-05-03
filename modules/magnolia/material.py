from typing import TypedDict

import bpy

from .objects import ObjectArg, resolve_object


# Note: This is an incomplete list of configuration options. As needed, more input properties may
# need to be added to this type in the future.
# Additionally, these fields should all be `NotRequired`, but that's not supported by Blender's
# version of Python.
PrincipledBSDFMaterialConfig = TypedDict(
    "PrincipledBSDFMaterialConfig",
    {
        "Base Color": tuple[float, float, float, float],
        "Roughness": float,
        "Emission Color": tuple[float, float, float, float],
        "Emission Strength": float,
    },
)


def assign_material(arg: ObjectArg, material: bpy.types.Material):
    obj = resolve_object(arg)
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)


def create_bsdf_material(
    name: str,
    config: PrincipledBSDFMaterialConfig,
    shadow: str = "OPAQUE",  # "OPAQUE" or "NONE"
) -> bpy.types.Material:
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    for key, value in config.items():
        bsdf.inputs[key].default_value = value
    material.shadow_method = shadow
    return material


def create_emission_material(
    name: str,
    color: tuple[float, float, float, tuple],
    shadow: str = "OPAQUE",  # "OPAQUE" or "NONE"
) -> bpy.types.Material:
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True

    # Create a new emission node
    emission_node = material.node_tree.nodes.new("ShaderNodeEmission")
    emission_node.inputs["Color"].default_value = color
    material.shadow_method = shadow

    # Link emission node to material output
    material.node_tree.links.new(
        emission_node.outputs["Emission"],
        material.node_tree.nodes["Material Output"].inputs["Surface"],
    )

    return material


def get_or_create_bsdf_material(
    name: str,
    config: PrincipledBSDFMaterialConfig,
    shadow: str = "OPAQUE",
) -> bpy.types.Material:
    """
    Gets an existing material or creates it from a configuration if needed.
    """
    material = bpy.data.materials.get(name)
    if material is not None:
        return material
    return create_bsdf_material(name, config, shadow=shadow)


def get_or_create_emission_material(
    name: str,
    color: tuple[float, float, float],
    shadow: str = "OPAQUE",  # "OPAQUE" or "NONE"
) -> bpy.types.Material:
    """
    Gets an existing material or creates it from a configuration if needed.
    """
    material = bpy.data.materials.get(name)
    if material is not None:
        return material
    return create_emission_material(name, color, shadow=shadow)
