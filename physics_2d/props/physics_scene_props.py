import bpy
from bpy.props import *
from bpy.utils import register_class, unregister_class

from ..types import PlanDirection

physics_property_name = 'three_physics'

# from ..draw_handlers import update_shape_draw

# def update_func_shape_visibility(self, context):
#     print(self.physics_2d_display_shape)
#     return



class Physics2DViewportSettingsPropertyGroup(bpy.types.PropertyGroup):
    display_shape_gizmos: BoolProperty(name="Display shape gizmos",description="Display shape gizmos", default=True)
    display_shape: BoolProperty(name="Display shape",description="Display shape", default=True)
    display_joint_gizmos: BoolProperty(name="Display joint gizmos",description="Display joint gizmos", default=True)
    display_joint: BoolProperty(name="Display joint",description="Display joint", default=True)


class PhysicsScenePropertyGroup(bpy.types.PropertyGroup):
    
    # Physics mode
    # physics_mode: EnumProperty(name="Physics mode", items = ThreePhysicsMode, default='disabled')
    physics_2d_enabled: BoolProperty(name="Box 2D",description="Box 2D enabled", default=False)

    # 2D options
    physics_2d_gravity: FloatVectorProperty(name="Gravity", default=(0,0), size=2)
    physics_2d_orientation: EnumProperty(name="Orientation", items = PlanDirection, default='Z') 
    physics_2d_display_shape: BoolProperty(name="Display shape",description="Display shape", default=False)

    # physics_2d_joints: PointerProperty(type=Physics2DJointsPropertyGroup)
    physics_2d_viewport_settings: PointerProperty(type=Physics2DViewportSettingsPropertyGroup)

    # 3D options
    # physics_3d_enabled: BoolProperty(name="Ammo",description="Ammo enabled", default=False)

    
classes = (
    Physics2DViewportSettingsPropertyGroup,
    PhysicsScenePropertyGroup,
)


def register_physics_scene_props():
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.three_physics = PointerProperty(type=PhysicsScenePropertyGroup)
def unregister_physics_scene_props():
    for cls in reversed(classes):
        unregister_class(cls)
        
    delattr(bpy.types.Scene, physics_property_name)
