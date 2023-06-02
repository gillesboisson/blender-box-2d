import bpy

from .op import ThreePhysicsCreateBoxVerticesOperator
from .physics_2d_shape import AddVertexToPolygonShapeOperator, RemoveVertexToPolygonShapeOperator, EditPolygon2DVertexOperator


def register_operators() -> None:
    bpy.utils.register_class(ThreePhysicsCreateBoxVerticesOperator)
    bpy.utils.register_class(AddVertexToPolygonShapeOperator)
    bpy.utils.register_class(RemoveVertexToPolygonShapeOperator)
    bpy.utils.register_class(EditPolygon2DVertexOperator)


def unregister_operators() -> None:
    bpy.utils.unregister_class(ThreePhysicsCreateBoxVerticesOperator)
    bpy.utils.unregister_class(AddVertexToPolygonShapeOperator)
    bpy.utils.unregister_class(RemoveVertexToPolygonShapeOperator)
    bpy.utils.unregister_class(EditPolygon2DVertexOperator)