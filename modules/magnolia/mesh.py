from typing import Optional

import bpy

from bpy.types import Object

from .objects import ObjectArg, resolve_object
from .scene import CollectionArg, resolve_collection, selection


# A vertex is represented as a tuple of (x, y, z)
Vertex = tuple[float, float, float]

# An edge is represented as a pair of vertex indices
Edge = tuple[int, int]

# A face is represented as a variable-length tuple of vertex indices
Face = tuple[int, ...]

# Meshes contain data about their vertices, edges, and faces
MeshData = tuple[list[Vertex], list[Edge], list[Face]]


def object_to_mesh_data(arg: Optional[ObjectArg] = None) -> MeshData:
    """
    Return the mesh data associated with an object.

    Optional arguments:

    - `arg`: The object whose mesh data should be returned. Defaults to current
      selection.

    Returns:

    - `vertices`: List of vertices, each a tuple (x, y, z)
    - `edges`: List of edges, each a tuple pair of vertex indices
    - `faces`: List of faces, each a tuple of vertex indices
    """
    obj = resolve_object(arg or selection())
    mesh = obj.data
    vertices = [vertex.co[:] for vertex in mesh.vertices]
    edges = [edge.vertices[:] for edge in mesh.edges]
    faces = [face.vertices[:] for face in mesh.polygons]
    return vertices, edges, faces


def create_object_from_mesh_data(
    data: MeshData,
    name: Optional[str] = None,
    collection: Optional[CollectionArg] = None,
    shade_flat: bool = False,
) -> Object:
    """
    Converts mesh data to a new Blender object with that mesh.

    Arguments:

    - `data`: The mesh data for the new object

    Optional arguments:

    - `name`: The name for the new object
    - `collection`: The collection to link the new object to
    - `shade_flat`: Whether to shade flat or smooth

    Returns: The newly created object
    """
    vertices, edges, faces = data
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, edges, faces, shade_flat=shade_flat)
    obj = bpy.data.objects.new(name, mesh)
    coll = resolve_collection(collection)
    coll.objects.link(obj)
    return obj
