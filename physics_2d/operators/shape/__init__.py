from .physic_2d_create_shape_poly_operator import Physics2DCreateShapePolyOperator
from .physics_2d_create_box_shape import Physics2DCreateBoxShapeOperator
from .physics_2d_create_circle_shape import Physics2DCreateCircleShapeOperator
from .physics_2d_delete_shape_operator import Physics2DDeleteShapeOperator

classes = (
    Physics2DCreateShapePolyOperator,
    Physics2DCreateBoxShapeOperator,
    Physics2DDeleteShapeOperator,
    Physics2DCreateCircleShapeOperator
)

from bpy.utils import register_class, unregister_class

def register_shapes_operators() -> None:
    for panelClass in classes:
        register_class(panelClass)


def unregister_shapes_operators() -> None:
    revertClasses = reversed(classes)
    for panelClass in revertClasses:
        unregister_class(panelClass)

