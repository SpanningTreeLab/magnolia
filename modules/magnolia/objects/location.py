from .objects import ObjectArg, resolve_object


def move_to_object(source_arg: ObjectArg, target_arg: ObjectArg):
    """
    Moves the source object to be in the same world location as the target object.

    Uses actual global coordinates, rather than relative location values.
    """
    source = resolve_object(source_arg)
    target = resolve_object(target_arg)

    # Get absolute positions
    source_loc = list(source.matrix_world.decompose()[0])  # pyright: ignore
    target_loc = list(target.matrix_world.decompose()[0])  # pyright: ignore

    # Get delta in position
    x_diff = target_loc[0] - source_loc[0]
    y_diff = target_loc[1] - source_loc[1]
    z_diff = target_loc[2] - source_loc[2]

    # Move by delta
    source.location[0] += x_diff
    source.location[1] += y_diff
    source.location[2] += z_diff
