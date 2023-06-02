from cProfile import label
import bpy
from bpy.props import *
from bpy.utils import register_class, unregister_class

from ..utils.enums import body_orientation_enum, three_physics_mode_enum

physics_property_name = 'three_physics'

class PhysicsScenePropertyGroup(bpy.types.PropertyGroup):
    physics_mode: EnumProperty(name="Physics mode", items = three_physics_mode_enum, default='disabled')
    physics_2d_gravity: FloatVectorProperty(name="Gravity", default=(0,0), size=2)
    physics_2d_orientation: EnumProperty(name="Orientation", items = body_orientation_enum, default='z') 
    physics_3d_enabled: BoolProperty(name="Ammo",description="Ammo enabled", default=False)
   
    

def register_physics_scene_props():
    register_class(PhysicsScenePropertyGroup)
    bpy.types.Scene.three_physics = PointerProperty(type=PhysicsScenePropertyGroup)
def unregister_physics_scene_props():
    unregister_class(PhysicsScenePropertyGroup)
    delattr(bpy.types.Scene, physics_property_name)
