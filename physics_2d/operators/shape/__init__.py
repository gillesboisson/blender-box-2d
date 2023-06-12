from .physic_2d_create_shape_poly_operator import Physics2DCreateShapePolyOperator

classes = (
    Physics2DCreateShapePolyOperator,
)

from bpy.utils import register_class, unregister_class

def register_shapes_operators() -> None:
    for panelClass in classes:
        register_class(panelClass)


def unregister_shapes_operators() -> None:
    revertClasses = reversed(classes)
    for panelClass in revertClasses:
        unregister_class(panelClass)

