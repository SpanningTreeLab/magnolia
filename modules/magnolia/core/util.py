import bpy


def current_frame() -> int:
    """
    Returns the current frame number of the current scene.
    """
    return bpy.context.scene.frame_current
