from .objects import ObjectArg, resolve_object

import bpy


def constrain_child(
    arg: ObjectArg,
    target_arg: ObjectArg,
    clear_inverse: bool = True,
) -> bpy.types.ChildOfConstraint:
    """
    Adds a child constraint to an object.

    Arguments:

    - `arg`: Object to be the child
    - `target_arg`: Object to be the parent

    Optional arguments:

    - `clear_inverse`: If `True`, then the child's `location` value is treated as relative to
      the parent, which may result in the child moving. If `false`, the child's `location`
      value is treated as its current position (i.e. there's an inverse correction).
    """
    obj = resolve_object(arg)
    target = resolve_object(target_arg)
    constraint = obj.constraints.new("CHILD_OF")
    constraint.target = target
    if clear_inverse:
        constraint.inverse_matrix.identity()
    return constraint
