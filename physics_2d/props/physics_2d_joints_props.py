from cProfile import label
import bpy
from bpy.props import *
from bpy.utils import register_class, unregister_class
from ..utils import object_can_have_joint


    
class Physics2DRevoluteJointPropertyGroup(bpy.types.PropertyGroup):
    name: StringProperty(name="Name", default="Revolute joint")
    body_a: PointerProperty(name="Body A", type=bpy.types.Object, poll=object_can_have_joint)
    body_b: PointerProperty(name="Body B", type=bpy.types.Object, poll=object_can_have_joint)
    anchor_a: FloatVectorProperty(name="Anchor A", default=(0,0), size=2)
    collide_connected: BoolProperty(name="Collide connected", default=False)
    reference_angle: FloatProperty(name="Reference angle", default=0)
    enable_limit: BoolProperty(name="Enable limit", default=False)
    lower_angle: FloatProperty(name="Lower angle", default=0)
    upper_angle: FloatProperty(name="Upper angle", default=0)
    enable_motor: BoolProperty(name="Enable motor", default=False)
    motor_speed: FloatProperty(name="Motor speed", default=0)
    max_motor_torque: FloatProperty(name="Max motor torque", default=0)

class Physics2DDistanceJointPropertyGroup(bpy.types.PropertyGroup):
    name: StringProperty(name="Name", default="Distance joint")
    body_a: PointerProperty(name="Body A", type=bpy.types.Object, poll=object_can_have_joint)
    body_b: PointerProperty(name="Body B", type=bpy.types.Object, poll=object_can_have_joint)
    anchor_a: FloatVectorProperty(name="Anchor A", default=(0,0), size=2)
    anchor_b: FloatVectorProperty(name="Anchor B", default=(0,0), size=2)
    collide_connected: BoolProperty(name="Collide connected", default=False)
    
    enable_limit: BoolProperty(name="Enable limit", default=False)
    lower: FloatProperty(name="Lower", default=0)
    upper: FloatProperty(name="Upper", default=0)

    stiffness: FloatProperty(name="Stiffness", default=0)
    damping_ratio: FloatProperty(name="Damping ratio", default=0)


class Physics2DPrismaticJointPropertyGroup(bpy.types.PropertyGroup):
    name: StringProperty(name="Name", default="Prismatic joint")
    body_a: PointerProperty(name="Body A", type=bpy.types.Object, poll=object_can_have_joint)
    body_b: PointerProperty(name="Body B", type=bpy.types.Object, poll=object_can_have_joint)
    anchor_a: FloatVectorProperty(name="Anchor A", default=(0,0), size=2)
    # anchor_b: FloatVectorProperty(name="Anchor B", default=(0,0), size=2)
    collide_connected: BoolProperty(name="Collide connected", default=False)
    reference_angle: FloatProperty(name="Reference angle", default=0)
    enable_limit: BoolProperty(name="Enable limit", default=False)
    lower: FloatProperty(name="lower", default=0)
    upper: FloatProperty(name="upper", default=0)
    enable_motor: BoolProperty(name="Enable motor", default=False)
    motor_speed: FloatProperty(name="Motor speed", default=0)
    max_motor_force: FloatProperty(name="Max motor force", default=0)
    local_axis: FloatVectorProperty(name="Local axis", default=(0,1), size=2)



class Physics2DWheelsJointPropertyGroup(bpy.types.PropertyGroup):
    name: StringProperty(name="Name", default="Wheel joint")
    body_a: PointerProperty(name="Body A", type=bpy.types.Object, poll=object_can_have_joint)
    body_b: PointerProperty(name="Body B", type=bpy.types.Object, poll=object_can_have_joint)
    anchor_a: FloatVectorProperty(name="Anchor A", default=(0,0), size=2)
    # anchor_b: FloatVectorProperty(name="Anchor B", default=(0,0), size=2)
    collide_connected: BoolProperty(name="Collide connected", default=False)
  
    local_axis: FloatVectorProperty(name="Local axis", default=(0,1), size=2)
    
    enable_limit: BoolProperty(name="Enable limit", default=False)
    lower: FloatProperty(name="lower", default=0)
    upper: FloatProperty(name="upper", default=0)

    enable_motor: BoolProperty(name="Enable motor", default=False)
    motor_speed: FloatProperty(name="Motor speed", default=0)
    max_motor_torque: FloatProperty(name="Max motor torque", default=0)

    stiffness: FloatProperty(name="Stiffness", default=0)
    damping_ratio: FloatProperty(name="Damping ratio", default=0)



class Physics2DJointsPropertyGroup(bpy.types.PropertyGroup):
    revolute_joints: CollectionProperty(name="Revolute joints", type=Physics2DRevoluteJointPropertyGroup)
    prismatic_joints: CollectionProperty(name="Prismatic joints", type=Physics2DPrismaticJointPropertyGroup)
    distance_joints: CollectionProperty(name="Distance joints", type=Physics2DDistanceJointPropertyGroup)
    wheel_joints: CollectionProperty(name="Wheels joints", type=Physics2DWheelsJointPropertyGroup)

classes = (
    Physics2DRevoluteJointPropertyGroup,
    Physics2DPrismaticJointPropertyGroup,
    Physics2DDistanceJointPropertyGroup,
    Physics2DWheelsJointPropertyGroup,
    Physics2DJointsPropertyGroup
)


def register_physics_2d_joints_props():
    for cls in classes:
        register_class(cls)

    bpy.types.Object.physics_2d_joints = PointerProperty(type=Physics2DJointsPropertyGroup)

def unregister_physics_2d_joints_props():
    for cls in reversed(classes):
        unregister_class(cls)

    delattr(bpy.types.Object, 'physics_2d_joints')
    

