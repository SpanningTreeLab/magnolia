import bpy
import magnolia


def setup_slide():
    """
    Sets up a Magnolia slide in Blender.
    """
    coll = bpy.data.collections.new("Production")
    bpy.context.scene.collection.children.link(coll)

    def setup_colors():
        # Set color management settings
        bpy.context.scene.view_settings.view_transform = "Standard"  # pyright: ignore

    def setup_slide_background():
        background_data: magnolia.mesh.MeshData = (
            [
                (0, 0, 0),
                (0, 1, 0),
                (1, 1, 0),
                (1, 0, 0),
            ],
            [(0, 1), (1, 2), (2, 3), (3, 0)],
            [(0, 1, 2, 3)],
        )
        base = magnolia.mesh.create_object_from_mesh_data(
            background_data, name="Background", collection=coll
        )

    setup_colors()
    setup_slide_background()
