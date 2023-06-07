

from .physics_2d_shape_widgets import register_physic_2d_shape_widgets, unregister_physic_2d_shape_widgets



def register_widgets() -> None:
    register_physic_2d_shape_widgets()

def unregister_widgets() -> None:
    unregister_physic_2d_shape_widgets()