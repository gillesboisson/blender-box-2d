import bpy
from .physics_2d_add_vertex_to_polygon_shape_operator import ThreePhysics2DAddVertexToPolygonShapeOperator
from .physics_2d_display_polygon_vertex_operator import ThreePhysics2DDisplayPolygonVertexOperator
from .physics_2d_edit_polygon_vertex_operator import ThreePhysics2DEditPolygonVertexOperator
from .physics_2d_remove_vertex_to_polygon_shape_operator import ThreePhysics2DRemoveVertexToPolygonShapeOperator
from .physics_2d_shape_move_operator import Physics2DShapeMoveOperator



operatorClasses = [
    # ThreePhysics2DAddVertexToPolygonShapeOperator,
    ThreePhysics2DRemoveVertexToPolygonShapeOperator,
    ThreePhysics2DEditPolygonVertexOperator,
    # ThreePhysics2DDisplayPolygonVertexOperator
    # Physics2DShapeMoveOperator
]

def register_operators():
    for operatorClass in operatorClasses:
        bpy.utils.register_class(operatorClass)

def unregister_operators():
    revertClasses = reversed(operatorClasses)
    for operatorClass in revertClasses:
        bpy.utils.unregister_class(operatorClass)

