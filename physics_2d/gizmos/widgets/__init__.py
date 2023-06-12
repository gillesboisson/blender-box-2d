

from .physics_2d_shape_widgets import register_physic_2d_shape_widgets, unregister_physic_2d_shape_widgets
from .joints import register_physic_2d_joint_widgets, unregister_physic_2d_joint_widgets


def register_widgets() -> None:
    register_physic_2d_shape_widgets()
    register_physic_2d_joint_widgets()

def unregister_widgets() -> None:
    unregister_physic_2d_shape_widgets()
    unregister_physic_2d_joint_widgets()