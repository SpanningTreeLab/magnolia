from typing import cast

import bpy

from ..objects.material import create_emission_material, get_or_create_emission_material


Color = tuple[int, int, int]
"""A color used in a Magnolia slide is a tuple of red, green, blue values,
where each value is in the range [0, 255]."""


def color_material(
    color: Color = (0, 0, 0),
    name: str | None = None,
    opacity_controls: bool = True,
):
    """
    Gets or creates an emission color material.

    Optional arguments:

    - `name`: The name of the material.
      A default name is supplied if none provided.
    - `color`: The color of the material.
    - `opacity_controls`: Whether to add opacity controls to the material.
      Defaults to True.
    """
    red, green, blue = color
    name = name or f"MgColorMat_{red}_{green}_{blue}"
    return get_or_create_emission_material(
        name,
        (red / 255, green / 255, blue / 255, 1),
        shadow="NONE",
        opacity_control=opacity_controls,
    )
