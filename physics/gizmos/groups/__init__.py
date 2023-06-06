
import bpy
from .physics_2d_square_edit_gizmo import Physics2DSquareEditGizmo
from .physics_2d_circle_edit_gizmo import Physics2DCircleEditGizmo



classes = (
    Physics2DSquareEditGizmo,
    Physics2DCircleEditGizmo
)


def register_groups():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister_groups():
    reverted_classes = reversed(classes)
    for cls in reverted_classes:
        bpy.utils.unregister_class(cls)

    