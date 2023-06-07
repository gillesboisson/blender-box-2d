from cProfile import label
import bpy
from bpy.props import *
from bpy.utils import register_class, unregister_class

# from ...physics.types import PlanDirection

# from ..types import Physics3DBodyShapeType

# rigid_body_property_name = 'three_rigid_body_3d'

# class RigidBody3DPropertyGroup(bpy.types.PropertyGroup):
#     enabled: BoolProperty(name="Rigid body",description="Physics enabled", default=False)
#     shape_type: EnumProperty(name="Shape", items = Physics3DBodyShapeType, default='box')
#     mass: FloatProperty(name="Mass", default=0,min=0,max=100)
#     shape_translation: FloatVectorProperty(name="Location", default=(0,0,0))

#     shape_box_scale: FloatVectorProperty(name="Scale", default=(1,1,1), min=0)
#     # shape_box_margin: FloatVectorProperty(name="Margin", default=(0,0,0))
#     shape_orientation: EnumProperty(name="Orientation", items = PlanDirection, default='Y')
#     shape_radius: FloatProperty(name="Radius",default=0.5, min=0)
#     shape_length: FloatProperty(name="Length",default=1, min=0)
#     shape_mesh_object: BoolProperty(name="Use object mesh",default=True)
#     shape_mesh: StringProperty(name="Shape mesh (geom name)",default="")
    






# def register_physics_3d_body_props():
#     register_class(RigidBody3DPropertyGroup)
#     bpy.types.Object.three_rigid_body_3d = PointerProperty(type=RigidBody3DPropertyGroup)
#     bpy.types.Mesh.three_rigid_body_3d = PointerProperty(type=RigidBody3DPropertyGroup)
# def unregister_physics_3d_body_props():
#     unregister_class(RigidBody3DPropertyGroup)
#     delattr(bpy.types.Object, rigid_body_property_name)
#     delattr(bpy.types.Mesh, rigid_body_property_name)


