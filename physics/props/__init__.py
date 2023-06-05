from .physics_3d_body_props import register_physics_3d_body_props, unregister_physics_3d_body_props
from .physics_2d_body_props import register_physics_2d_body_props, unregister_physics_2d_body_props
# from .entity_props import register_entity_props, unregister_entity_props
from .physics_scene_props import register_physics_scene_props, unregister_physics_scene_props

def register_props() -> None:
    # register_entity_props()
    register_physics_scene_props()
    register_physics_3d_body_props()
    register_physics_2d_body_props()

def unregister_props() -> None:
    # unregister_entity_props()
    unregister_physics_scene_props()
    unregister_physics_3d_body_props()
    unregister_physics_2d_body_props()