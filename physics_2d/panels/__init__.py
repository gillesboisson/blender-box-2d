
from .physics_2d import register_physics_2d_panels, unregister_physics_2d_panels

def register_panels() -> None:
    register_physics_2d_panels()

def unregister_panels() -> None:
    unregister_physics_2d_panels()

