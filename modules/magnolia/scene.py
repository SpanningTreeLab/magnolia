from typing import Optional, Union

import bpy

from bpy.types import Object


# An collection argument can be that collection's identifier, or the collection itself
CollectionArg = Union[str, bpy.types.Collection]


def current_frame() -> int:
    """
    Returns the current frame number of the current scene.
    """
    return bpy.context.scene.frame_current


def selections() -> list[Object]:
    """
    Returns a list of currently selected objects.
    """
    return list(bpy.context.selected_objects)


def selection() -> Object:
    """
    Returns the currently selected object.

    Raises an `Exception` if no objects are selected or more than one object is selected.
    """
    objects = selections()
    if len(objects) != 1:
        raise Exception("More than one object selected")
    return objects[0]


def resolve_collection(arg: Optional[CollectionArg] = None) -> bpy.types.Collection:
    """
    Returns a collection, given the collection or a collection identifier.
    If neither is specified, the current context's collection is used.

    Optional arguments:

    - `arg`: A collection or collection ID

    Returns: The resulting collection
    """
    if arg is None:
        return bpy.context.scene.collection
    if isinstance(arg, bpy.types.Collection):
        return arg
    return bpy.data.collections[arg]
