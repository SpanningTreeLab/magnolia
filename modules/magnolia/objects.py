from typing import Optional, Union

import bpy

from bpy.types import Object


# An object can be that object's identifier, or the object itself
ObjectArg = Union[str, Object]

# An object argument, or a list of object arguments
ObjectsArg = Union[ObjectArg, list[ObjectArg]]


def resolve_object(arg: ObjectArg) -> Object:
    """
    Returns an object, given the object or an object identifier.

    Arguments:

    - `arg`: A Blender object or object ID

    Returns: Blender object, or `None` if unsuccessful
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
