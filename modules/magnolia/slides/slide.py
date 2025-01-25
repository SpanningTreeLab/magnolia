from typing import cast

import bpy

from ..objects.material import assign_material
from ..objects.mesh import create_object_from_mesh_data, MeshData
from ..scene.camera import create_camera
from ..scene.collection import create_collection
from ..scene.output import set_framerate
from .colors import Color, color_material


def setup_slide(
    color: Color = (255, 255, 255),
    width: int = 3840,
    height: int = 2160,
    framerate: int = 60,
):
    """
    Sets up a Magnolia slide in Blender.

    Optional arguments:

    - `color`: The background color of the slide. Defaults to white.
    - `framerate`: The framerate of the slide. Defaults to 60.
    """
    coll = create_collection("Production")

    # Set color management settings
    bpy.context.scene.view_settings.view_transform = "Standard"  # pyright: ignore

    set_slide_dimensions(width, height)

    # Create slide
    slide_width = width / 100
    slide_height = height / 100
    background_data: MeshData = (
        [
            (0, 0, 0),
            (0, slide_height, 0),
            (slide_width, slide_height, 0),
            (slide_width, 0, 0),
        ],
        [(0, 1), (1, 2), (2, 3), (3, 0)],
        [(0, 1, 2, 3)],
    )
    base = create_object_from_mesh_data(
        background_data, name="Background", collection=coll
    )
    assign_material(base, color_material(color))
    # Disable selection of slide
    base.hide_select = True

    # Set up camera
    camera_obj = create_camera("Camera", collection=coll)
    camera_obj.location = (slide_width / 2, slide_height / 2, 20)
    camera_data = cast(bpy.types.Camera, camera_obj.data)
    camera_data.type = "ORTHO"
    # Set scale so that camera covers entire region
    # TODO: Figure out how this needs to scale for different widths, heights
    camera_data.ortho_scale = 38.3

    # Set world surface background color to black
    world_bg = bpy.context.scene.world.node_tree.nodes["Background"]  # pyright: ignore
    world_bg.inputs["Color"].default_value = (0, 0, 0, 1)  # pyright: ignore

    # Set framerate
    set_framerate(framerate)


def set_slide_dimensions(width: int, height: int):
    """
    Sets the dimensions of the slide.
    """
    bpy.context.scene.render.resolution_x = width
    bpy.context.scene.render.resolution_y = height


def get_slide_dimensions() -> tuple[int, int]:
    """
    Returns the dimensions of the slide.
    """
    return (
        bpy.context.scene.render.resolution_x,
        bpy.context.scene.render.resolution_y,
    )
