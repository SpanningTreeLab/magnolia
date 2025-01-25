import bpy


def set_framerate(rate: int = 30):
    """
    Sets the framerate of the current scene.

    Optional arguments:

    - `rate`: The framerate to set. Defaults to 30.
    """
    bpy.context.scene.render.fps = rate
    bpy.context.scene.render.fps_base = 1
