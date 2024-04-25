import importlib
import sys


def reload():
    """
    Reloads the Magnolia module and all submodules.
    """
    for module_name, module in list(sys.modules.items()):
        if module_name.startswith(__name__):
            importlib.reload(module)
    importlib.reload(sys.modules[__name__])


__all__ = [
    "animation",
    "material",
    "mesh",
    "modifier",
    "objects",
    "scene",
    "visibility",
]


from .animation import *
from .material import *
from .mesh import *
from .modifier import *
from .objects import *
from .scene import *
from .visibility import *
