
from .joints import register_joints_operators, unregister_joints_operators
from .shape import register_shapes_operators, unregister_shapes_operators




def register_operators() -> None:
    register_joints_operators()
    register_shapes_operators()

def unregister_operators() -> None:
    unregister_joints_operators()
    unregister_shapes_operators()