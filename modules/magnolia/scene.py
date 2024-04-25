import bpy

from bpy.types import Object


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
