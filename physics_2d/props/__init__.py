from .physics_2d_body_props import register_physics_2d_body_props, unregister_physics_2d_body_props
from .physics_scene_props import register_physics_scene_props, unregister_physics_scene_props
from .physics_2d_joints_props import register_physics_2d_joints_props, unregister_physics_2d_joints_props

def register_props() -> None:
    register_physics_2d_body_props()
    register_physics_2d_joints_props()
    register_physics_scene_props()

def unregister_props() -> None:
    unregister_physics_scene_props()
    unregister_physics_2d_joints_props()
    unregister_physics_2d_body_props()
