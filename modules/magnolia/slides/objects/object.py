from bpy.types import Object


def set_object_default_properties(obj: Object):
    # Set opacity
    obj["mg_opacity"] = 1.0

    # Set UI limits on opacity
    opacity_manager = obj.id_properties_ui("mg_opacity")
    opacity_manager.update(min=0.0, max=1.0)
