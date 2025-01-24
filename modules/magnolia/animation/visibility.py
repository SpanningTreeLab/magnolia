from typing import Optional

from ..objects import ObjectArg, ObjectsArg, resolve_object, resolve_objects
from ..scene import current_frame, selections


def toggle_object_visibility(
    arg: ObjectArg, frame: int, is_visible: bool, children: bool = True
):
    """
    Sets a frame at which an object should become visible or invisible.

    Arguments:

    - `arg`: Object to make visible or invisible
    - `frame`: Frame at which the visibility should be updated
    - `is_visible`: `True` if object should become visible, `False` if it should become invisible

    Optional arguments:

    - `children`: Whether children of the object should also have visibility animated, defaults to
      `True`
    """
    obj = resolve_object(arg)

    # At (frame - 1), add keyframe that is the opposite of the end visibility state
    obj.hide_viewport = is_visible
    obj.hide_render = is_visible
    obj.keyframe_insert("hide_viewport", frame=frame - 1)
    obj.keyframe_insert("hide_render", frame=frame - 1)

    # At (frame), add keyframe that is the end visibility state
    obj.hide_viewport = not is_visible
    obj.hide_render = not is_visible
    obj.keyframe_insert("hide_viewport", frame=frame)
    obj.keyframe_insert("hide_render", frame=frame)

    # If we should apply animation to children, then recursively call on children
    if children:
        for child in obj.children:
            toggle_object_visibility(child, frame, is_visible, children)


def show_at(arg: ObjectArg, frame: int, children: bool = True):
    """
    Animates an object to appear at frame `frame`.

    Arguments:

    - `arg`: Object to make visible
    - `frame`: Frame at which the object should be shown

    Optional arguments:

    - `children`: Whether children of the object should also have visibility animated, defaults to
      `True`
    """
    toggle_object_visibility(arg, frame, True, children)


def hide_at(arg: ObjectArg, frame: int, children: bool = True):
    """
    Animates an object to disappear at frame `frame`.

    Arguments:

    - `arg`: Object to hide
    - `frame`: Frame at which the object should be hidden

    Optional arguments:

    - `children`: Whether children of the object should also have visibility animated, defaults to
      `True`
    """
    toggle_object_visibility(arg, frame, False, children)


def show_now(arg: Optional[ObjectsArg] = None, children: bool = True):
    """
    Animates an object to appear at the current frame.

    Optional arguments:

    - `arg`: Object to make visible, defaults to current selection
    - `children`: Whether children of the object should also have visibility animated, defaults to
      `True`
    """
    objs = resolve_objects(arg) if arg is not None else selections()
    for obj in objs:
        show_at(obj, current_frame(), children)


def hide_now(arg: Optional[ObjectsArg] = None, children: bool = True):
    """
    Animates an object to hide at the current frame.

    Optional arguments:

    - `arg`: Object to hide, defaults to current selection
    - `children`: Whether children of the object should also have visibility animated, defaults to
      `True`
    """
    objs = resolve_objects(arg) if arg is not None else selections()
    for obj in objs:
        hide_at(obj, current_frame(), children)
