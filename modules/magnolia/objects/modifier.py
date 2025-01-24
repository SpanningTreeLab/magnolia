from typing import cast, Literal, Optional

import bpy

from .object import ObjectArg, resolve_object


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
    modifier = cast(
        bpy.types.SubsurfModifier, obj.modifiers.new(name or "Subdivision", "SUBSURF")
    )
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
    modifier = cast(
        bpy.types.ShrinkwrapModifier,
        obj.modifiers.new(name or "Shrinkwrap", "SHRINKWRAP"),
    )
    modifier.target = resolve_object(target_arg)
    modifier.offset = offset
    return modifier


def apply_hook(
    arg: ObjectArg,
    target_arg: ObjectArg,
    name: Optional[str] = None,
    vertex_indices: Optional[list[int]] = None,
) -> bpy.types.HookModifier:
    """
    Applies a hook modifier. Hooks an object (or particular vertices on that object) to a target.

    Arguments:

    - `arg`: The object for which to add a hook modifier
    - `target_arg`: The object that should be targeted by the hook

    Optional arguments:

    - `name`: Name for the modifier, default to "Hook"
    -` vertex_indices`: List of vertex indices to hook
    """
    obj = resolve_object(arg)
    target = resolve_object(target_arg)
    modifier = cast(bpy.types.HookModifier, obj.modifiers.new(name or "Hook", "HOOK"))
    modifier.object = target
    if vertex_indices:
        modifier.vertex_indices_set(vertex_indices)
    return modifier


def apply_bevel(
    arg: ObjectArg,
    name: Optional[str] = None,
    amount: float = 0.1,
    affect: Literal["VERTICES", "EDGES"] = "EDGES",
    segments: int = 4,
) -> bpy.types.BevelModifier:
    """
    Applies a bevel modifier.

    Arguments:

    - `arg`: The object for which to add a bevel modifier

    Optional arguments:

    - `name`: Name for the modifier, default to "Bevel"
    - `amount`: Width of the bevel
    - `affect`: Whether to round edges of vertices, must be "VERTICES" or "EDGES", defaults "EDGES"
    - `segments`: Number of segments to include in bevel
    """
    obj = resolve_object(arg)
    modifier = cast(
        bpy.types.BevelModifier, obj.modifiers.new(name or "Bevel", "BEVEL")
    )
    modifier.affect = affect
    modifier.width = amount
    modifier.segments = segments
    return modifier


def apply_skin(
    arg: ObjectArg,
    name: Optional[str] = None,
) -> bpy.types.SkinModifier:
    obj = resolve_object(arg)
    modifier = cast(bpy.types.SkinModifier, obj.modifiers.new(name or "Skin", "SKIN"))
    return modifier
