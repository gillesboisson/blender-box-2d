
import bpy
from .physics_2d_square_edit_gizmo import Physics2DSquareEditGizmo
from .physics_2d_circle_edit_gizmo import Physics2DCircleEditGizmo
from .physics_2d_polygon_edit_gizmo import Physics2DPolygonEditGizmo
from .physics_2d_shape_display_gizmo import  Physics2DShapeDisplayEmptyWidget,Physics2DShapeDisplayGizmo, clear_physic_2d_shape_draw_handler


classes = (
    Physics2DSquareEditGizmo,
    Physics2DCircleEditGizmo,
    Physics2DPolygonEditGizmo,
    Physics2DShapeDisplayEmptyWidget,
    Physics2DShapeDisplayGizmo,
    
)


def register_body_groups():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister_body_groups():
    clear_physic_2d_shape_draw_handler()
    reverted_classes = reversed(classes)
    for cls in reverted_classes:
        bpy.utils.unregister_class(cls)

    