from bpy.utils import register_class, unregister_class

from .rigid_body_3d_gizmo import  RigidBody3DWidgetGroup
from .rigid_body_2d_gizmo import  RigidBody2DWidgetGroup
from .cylinder_widget import  CylinderWidget
from .box_widget import BoxWidget
from .sphere_widget import SphereWidget
from .square_widget import SquareWidget
from .circle_widget import CircleWidget
from .polygon_widget import PolygonWidget
from .test_gizmo import MyCameraWidgetGroup


operatorClasses = (
    CylinderWidget,
    BoxWidget,
    SquareWidget,
    SphereWidget,
    CircleWidget,
    PolygonWidget,
    RigidBody3DWidgetGroup,
    RigidBody2DWidgetGroup,
    MyCameraWidgetGroup
)

def register_gizmos() -> None:
    for operatorClass in operatorClasses:
        register_class(operatorClass)

def unregister_gizmos() -> None:
    for operatorClass in operatorClasses:
        unregister_class(operatorClass)
