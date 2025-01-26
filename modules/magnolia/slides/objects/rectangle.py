from typing import Optional

from magnolia.slides.objects.object import set_object_default_properties

from ...objects.material import MaterialArg, assign_material, resolve_material
from ...objects.mesh import create_object_from_mesh_data
from ...scene.collection import resolve_collection
from ...scene.context import CollectionArg
from ..colors import Color, color_material
from ..position import Anchor, Position, resolve_position, set_anchor, scale_size


def create_rectangle(
    name: str = "Rectangle",
    material: MaterialArg | None = None,
    position: Position = (200, 200),
    width: float = 100,
    height: float = 100,
    anchor: Anchor = "center",
    collection: Optional[CollectionArg] = None,
):
    # Get rectangle material
    if material is None:
        material = color_material(color=(0, 0, 0))
    material = resolve_material(material)
    coll = resolve_collection(collection)

    # Create rectangle
    width, height = scale_size(width, height)
    rectangle_data = (
        [
            (0, 0, 0),
            (0, width, 0),
            (width, height, 0),
            (width, 0, 0),
        ],
        [(0, 1), (1, 2), (2, 3), (3, 0)],
        [(0, 1, 2, 3)],
    )
    obj = create_object_from_mesh_data(rectangle_data, name=name, collection=collection)
    set_anchor(obj, anchor)
    assign_material(obj, material)
    obj.location = resolve_position(position)
    set_object_default_properties(obj)
    return obj
