import bpy

from ..objects.material import get_or_create_emission_material


Color = tuple[int, int, int]
"""A color used in a Magnolia slide is a tuple of red, green, blue values,
where each value is in the range [0, 255]."""


def color_material(color: Color):
    """
    Gets or creates an emission color material.

    Arguments:

    - `red`: The red component of the color, 0-255
    - `green`: The green component of the color, 0-255
    - `blue`: The blue component of the color, 0-255
    """
    red, green, blue = color
    return get_or_create_emission_material(
        f"MgSlideColorMat_{red}_{green}_{blue}",
        (red / 255, green / 255, blue / 255, 1),
        shadow="NONE",
    )
