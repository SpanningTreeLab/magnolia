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
    name: str, config: PrincipledBSDFMaterialConfig
) -> bpy.types.Material:
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    for key, value in config.items():
        bsdf.inputs[key].default_value = value
    return material


def get_or_create_bsdf_material(
    name: str, config: PrincipledBSDFMaterialConfig
) -> bpy.types.Material:
    """
    Gets an existing material or creates it from a configuration if needed.
    """
    material = bpy.data.materials.get(name)
    if material is not None:
        return material
    return create_bsdf_material(name, config)
