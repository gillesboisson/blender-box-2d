from math import pi
import typing
from bpy.props import *
import bpy
from mathutils import Matrix
from .physics_2d_shape_move_widget import Physics2DShapeMoveWidget
from .physics_2d_circle_widget import Physics2DCircleWidget
from .physics_2d_square_widget import Physics2DSquareWidget
from .physics_2d_shape_radius_widget import Physics2DShapeRadiusWidget
from .physics_2d_shape_rotate_widget import Physics2DShapeRotateWidget
from .physics_2d_shape_scale_widget import Physics2DShapeScaleWidget
from .physics_2d_polygon_widget import Physics2DPolygonWidget
from .physics_2d_vertex_move_widget import Physics2DVertexMoveWidget
from .physics_2d_vertex_create_widget import Physics2DVertexCreateWidget



    
classes = (
    Physics2DShapeMoveWidget,
    Physics2DShapeRotateWidget,
    Physics2DSquareWidget,
    Physics2DCircleWidget,
    Physics2DShapeRadiusWidget,
    Physics2DShapeScaleWidget,
    Physics2DPolygonWidget,
    Physics2DVertexMoveWidget,
    Physics2DVertexCreateWidget,
)

def register_physic_2d_shape_widgets():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister_physic_2d_shape_widgets():
    for cls in classes:
        bpy.utils.unregister_class(cls)









