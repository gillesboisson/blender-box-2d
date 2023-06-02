from cProfile import label
import bpy
from bpy.props import *
from bpy.utils import register_class, unregister_class

entity_property_name = 'three_entity'

class ThreeEntityPropertyGroup(bpy.types.PropertyGroup):
    static: BoolProperty(name="Static",description="Static", default=True)
    cast_shadow: BoolProperty(name="Cast shadow",description="Cast shadow", default=False)
    layer_mask:IntProperty(name="Render layer mask",default=1)





def register_entity_props():
    register_class(ThreeEntityPropertyGroup)
    bpy.types.Object.three_entity = PointerProperty(type=ThreeEntityPropertyGroup)
def unregister_entity_props():
    unregister_class(ThreeEntityPropertyGroup)
    delattr(bpy.types.Object, entity_property_name)


