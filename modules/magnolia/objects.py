from typing import Optional, Union

import bpy

from bpy.types import Object

from .scene import CollectionArg, resolve_collection


# An object argument can be that object's identifier, or the object itself
ObjectArg = Union[str, Object]

# An object argument, or a list of object arguments
ObjectsArg = Union[ObjectArg, list[ObjectArg]]

# A scale argument could be a (x, y, z) scale tuple, or an x value for scale (x, x, x)
ScaleArg = Union[tuple[float, float, float], float]


def resolve_object(arg: ObjectArg) -> Object:
    """
    Returns an object, given the object or an object identifier.

    Arguments:

    - `arg`: An object or object ID

    Returns: The resulting object
    """
    if isinstance(arg, Object):
        return arg
    return bpy.data.objects[arg]


def resolve_objects(args: ObjectsArg) -> list[Object]:
    """
    Given an object argument or a list of object arguments, returns a list of corresponding
    objects.

    Arguments:

    - `args`: An object argument, or a list of object arguments

    Returns: List of objects
    """
    if isinstance(args, list):
        return [resolve_object(arg) for arg in args]
    return [resolve_object(args)]


def resolve_scale(arg: ScaleArg) -> tuple[float, float, float]:
    """
    Given a scale argument, returns a scale tuple.

    Arguments:

    - `arg`: The scale argument

    Returns: A tuple of (x, y, z) scale values
    """
    if isinstance(arg, tuple):
        return arg
    return (arg, arg, arg)


def copy_object(
    arg: ObjectArg,
    name: Optional[str] = None,
    collection: Optional[CollectionArg] = None,
    scale: Optional[ScaleArg] = None,
) -> Object:
    """
    Copies an object from a template object.

    Arguments:

    - `arg`: Template object to copy

    Optional arguments:

    - `name`: Name to give to the new object
    - `collection`: What collection to place the object in, defaults to the first collection of the
      object being copied
    - `scale`: Scale for the new object

    Returns: The newly copied object
    """
    # Get object to copy
    template_obj = resolve_object(arg)

    # Copy the object and its mesh data
    obj = template_obj.copy()
    obj.data = template_obj.data.copy()

    # Link the object to the new collection
    coll = resolve_collection(collection)
    coll.objects.link(obj)

    # Recursively create copies of all children
    for template_child in template_obj.children:
        child = copy_object(template_child, collection=collection)
        child.parent = obj
        child.matrix_parent_inverse = obj.matrix_world.inverted()

    # Possibly give the object a name
    if name is not None:
        obj.name = name
        obj.data.name = name

    # Possibly set scale
    if scale is not None:
        obj.scale = resolve_scale(scale)

    return obj
