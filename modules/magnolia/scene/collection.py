from typing import Optional

import bpy

from .context import CollectionArg


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
