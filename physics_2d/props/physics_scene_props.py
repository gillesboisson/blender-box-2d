from cProfile import label
import bpy
from bpy.props import *
from bpy.utils import register_class, unregister_class

from ..types import PlanDirection, ThreePhysicsMode

physics_property_name = 'three_physics'


def update_func_shape_visibility(self, context):
    print(self.physics_2d_display_shape)
    return

class PhysicsScenePropertyGroup(bpy.types.PropertyGroup):
    
    # Physics mode
    # physics_mode: EnumProperty(name="Physics mode", items = ThreePhysicsMode, default='disabled')
    physics_2d_enabled: BoolProperty(name="Box 2D",description="Box 2D enabled", default=False)

    # 2D options
    physics_2d_gravity: FloatVectorProperty(name="Gravity", default=(0,0), size=2)
    physics_2d_orientation: EnumProperty(name="Orientation", items = PlanDirection, default='Z') 
    physics_2d_display_shape: BoolProperty(name="Display shape",description="Display shape", default=False, update=update_func_shape_visibility)
    
    # 3D options
    # physics_3d_enabled: BoolProperty(name="Ammo",description="Ammo enabled", default=False)

    
   
    

def register_physics_scene_props():
    register_class(PhysicsScenePropertyGroup)
    bpy.types.Scene.three_physics = PointerProperty(type=PhysicsScenePropertyGroup)
def unregister_physics_scene_props():
    unregister_class(PhysicsScenePropertyGroup)
    delattr(bpy.types.Scene, physics_property_name)
