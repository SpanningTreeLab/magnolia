from typing import cast, Optional

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


def pop_in(
    args: Optional[ObjectsArg] = None,
    frame: Optional[int] = None,
    duration: int = 15,
    delay: Optional[int] = None,
):
    """
    Animates an object growing into place.

    Optional arguments:

    - `args`: Objects to animate, defaults to selected objects
    - `frame`: Frame at which animation should start, defaults to current frame
    - `duration`: Length of animation in frames, defaults to 15 frames
    - `delay`: Amount of time between animations, if multiple objects; defaults to 0
    """
    # Use current frame as default frame
    if frame is None:
        frame = current_frame()

    # Use selected objects as default
    if args is None:
        args = cast(list[ObjectArg], selections())

    # If we have a list of objects, animate each with a delay
    if isinstance(args, list):
        for i, arg in enumerate(args):
            if delay is not None:
                f = frame + i * delay
            else:
                f = frame
            pop_in(arg, frame=f, duration=duration)
        return

    # We know we have a single object now, so resolve it
    obj = resolve_object(cast(ObjectArg, args))

    # Animate starting position
    show_at(obj, frame)
    obj.scale[0] = 0
    obj.scale[1] = 0
    obj.scale[2] = 0
    obj.keyframe_insert("scale", frame=frame)

    # Animate end position
    obj.scale[0] = 1
    obj.scale[1] = 1
    obj.scale[2] = 1
    obj.keyframe_insert("scale", frame=frame + duration)


def pop_out(
    args: Optional[ObjectsArg] = None,
    frame: Optional[int] = None,
    duration: int = 15,
    delay: Optional[int] = None,
):
    """
    Animates an object shrinking and disappearing.

    Optional arguments:

    - `args`: Objects to animate, defaults to selected objects
    - `frame`: Frame at which animation should start, defaults to current frame
    - `duration`: Length of animation in frames, defaults to 15 frames
    - `delay`: Amount of time between animations, if multiple objects; defaults to 0
    """
    # Use current frame as default frame
    if frame is None:
        frame = current_frame()

    # Use selected objects as default
    if args is None:
        args = cast(list[ObjectArg], selections())

    # If we have a list of objects, animate each with a delay
    if isinstance(args, list):
        for i, arg in enumerate(args):
            if delay is not None:
                f = frame + i * delay
            else:
                f = frame
            pop_out(arg, frame=f, duration=duration)
        return

    # We know we have a single object now, so resolve it
    obj = resolve_object(args)

    # Animate starting position
    obj.scale[0] = 1
    obj.scale[1] = 1
    obj.scale[2] = 1
    obj.keyframe_insert("scale", frame=frame)

    # Animate end position
    obj.scale[0] = 0
    obj.scale[1] = 0
    obj.scale[2] = 0
    obj.keyframe_insert("scale", frame=frame + duration)
    hide_at(obj, frame + duration)
