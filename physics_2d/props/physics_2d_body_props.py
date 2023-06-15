from cProfile import label
import bpy
from bpy.props import *
from bpy.utils import register_class, unregister_class


from ..types import Physics2DBodyShapeType, PhysicsBodyType

rigid_body_2d_property_name = 'three_rigid_body_2d'


class Vertex2DPropertyGroup(bpy.types.PropertyGroup):
    pos: FloatVectorProperty(name="Position", size=2, default=(0,0))
    
class RigidBody2DShapePropertyGroup(bpy.types.PropertyGroup):
    # name: StringProperty(name="Name", default="Shape")
    friction: FloatProperty(name="Friction", default=0.2,min=0,max=10)
    restitution: FloatProperty(name="Restitution", default=0,min=0,max=10)
    density: FloatProperty(name="Density", default=1,min=0,max=10)
    sensor: BoolProperty(name="Sensor",description="Sensor", default=False)
    shape_type: EnumProperty(name="Shape", items = Physics2DBodyShapeType, default='box')
    filter_category_bits: IntProperty(name="Filter category bits", default=1,min=0,max=32)
    filter_mask_bits: IntProperty(name="Filter mask bits", default=65535,min=0,max=65535)
    filter_group_index: IntProperty(name="Filter group index", default=0,min=0,max=32767)
    shape_box_scale: FloatVectorProperty(name="Scale", size=2, default=(1,1))
    shape_position: FloatVectorProperty(name="Position", size=2, default=(0,0))
    shape_angle: FloatProperty(name="Angle", default=0,min=-180,max=180)
    shape_radius: FloatProperty(name="Radius",default=0.5, min=0)
    # shape_polygon_geometry: PointerProperty(name="Polygon geometry",type=bpy.types.Mesh)    
    shape_polygon_vertices: CollectionProperty(name="Polygon vertices",type=Vertex2DPropertyGroup)

class RigidBody2DPropertyGroup(bpy.types.PropertyGroup):
    enabled: BoolProperty(name="Three Rigid body",description="Three Rigid body", default=False)
    body_type: EnumProperty(name="Body type", items = PhysicsBodyType, default='static')
    bullet: BoolProperty(name="Bullet",description="Bullet physics", default=False)
    fixed_rotation: BoolProperty(name="Fixed rotation",description="Fixed rotation", default=False)
    sleeping_allowed: BoolProperty(name="Sleeping allowed",description="Sleeping allowed", default=True)
    linear_damping: FloatProperty(name="Linear damping", default=0,min=0,max=10)
    angular_damping: FloatProperty(name="Angular damping", default=0,min=0,max=10)
    mass: FloatProperty(name="Mass", default=0,min=0,max=100)
    active: BoolProperty(name="Active",description="Active", default=True)
    linear_velocity: FloatVectorProperty(name="Linear velocity", size=2, default=(0,0))
    angular_velocity: FloatProperty(name="Angular velocity", default=0)
    awake: BoolProperty(name="Awake",description="Awake", default=True)
    shapes: CollectionProperty(type=RigidBody2DShapePropertyGroup)


def register_physics_2d_body_props():
    register_class(Vertex2DPropertyGroup)
    register_class(RigidBody2DShapePropertyGroup)
    register_class(RigidBody2DPropertyGroup)
    bpy.types.Object.three_rigid_body_2d = PointerProperty(type=RigidBody2DPropertyGroup)
    bpy.types.Mesh.three_rigid_body_2d = PointerProperty(type=RigidBody2DPropertyGroup)

def unregister_physics_2d_body_props():
    unregister_class(Vertex2DPropertyGroup)
    unregister_class(RigidBody2DShapePropertyGroup)
    unregister_class(RigidBody2DPropertyGroup)
    delattr(bpy.types.Object, rigid_body_2d_property_name)
    delattr(bpy.types.Mesh, rigid_body_2d_property_name)


