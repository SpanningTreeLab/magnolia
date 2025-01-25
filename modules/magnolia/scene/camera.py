from typing import Optional

import bpy

from ..scene.collection import resolve_collection
from ..scene.context import CollectionArg


def create_camera(
    name: str, collection: Optional[CollectionArg] = None
) -> bpy.types.Object:
    """
    Creates a camera with the given name.

    Arguments:

    - `name`: The name of the camera

    Returns: The created camera
    """
    camera_data = bpy.data.cameras.new(name)
    camera = bpy.data.objects.new(name, camera_data)
    coll = resolve_collection(collection)
    coll.objects.link(camera)
    return camera
