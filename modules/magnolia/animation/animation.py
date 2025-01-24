from typing import cast, Optional

from ..objects import ObjectArg, ObjectsArg, resolve_object
from ..scene import current_frame, selections
from .visibility import show_at, hide_at


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
