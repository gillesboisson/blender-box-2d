from bpy.utils import register_class, unregister_class

from .rigid_body_3d_gizmo import  RigidBody3DWidgetGroup
from .rigid_body_2d_gizmo import  RigidBody2DWidgetGroup
from .plane_3d_square_gizmo import Plane3DSquareGizmo, MoveShapePositionOperator

from .widgets import register_widgets, unregister_widgets

operatorClasses = (
    RigidBody3DWidgetGroup,
    RigidBody2DWidgetGroup,
    Plane3DSquareGizmo,
    MoveShapePositionOperator
)

def register_gizmos() -> None:
    register_widgets()
    for operatorClass in operatorClasses:
        register_class(operatorClass)

def unregister_gizmos() -> None:
    unregister_widgets()
    for operatorClass in operatorClasses:
        unregister_class(operatorClass)
