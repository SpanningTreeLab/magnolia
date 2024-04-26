from typing import Optional

import bpy

from .objects import ObjectArg, resolve_object


def apply_subsurf(
    arg: ObjectArg,
    name: Optional[str] = None,
    levels: int = 3,
    viewport_levels: Optional[int] = None,
    use_catmull: bool = True,
    control_only: bool = True,
) -> bpy.types.SubsurfModifier:
    """
    Applies a subdivision surface modifier.

    Arguments:

    - `arg`: The object for which to add a subsurface modifier

    Optional arguments:

    - `name`: Name for the modifier, default to "Subdivision"
    - `levels`: Render levels of subdivision
    - `viewport_levels`: Viewport levels of subdivision, defaults to same as render level
    - `use_catmull`: Whether to use Catmull-Clark subdivision algorithm, default true
    - `control_only`: Whether to skip displaying interior subdivided edges, default true
    """
    obj = resolve_object(arg)
    modifier = obj.modifiers.new(name or "Subdivision", "SUBSURF")
    modifier.render_levels = levels
    modifier.levels = levels if viewport_levels is None else viewport_levels
    modifier.subdivision_type = "CATMULL_CLARK" if use_catmull else "SIMPLE"
    modifier.show_only_control_edges = control_only
    return modifier


def apply_shrinkwrap(
    arg: ObjectArg,
    target_arg: ObjectArg,
    name: Optional[str] = None,
    offset: float = 0.0,
) -> bpy.types.ShrinkwrapModifier:
    """
    Applies a shrinkwrap modifier.

    Arguments:

    - `arg`: The object for which to add a shrinkwrap modifier
    - `target_arg`: The object that should be targeted by the shrinkwrap

    Optional arguments:

    - `name`: Name for the modifier, default to "Shrinkwrap"
    - `offset`: The distance to keep from the target, default 0

    Returns: The shrinkwrap modifier
    """
    obj = resolve_object(arg)
    modifier = obj.modifiers.new(name or "Shrinkwrap", "SHRINKWRAP")
    modifier.target = resolve_object(target_arg)
    modifier.offset = offset
