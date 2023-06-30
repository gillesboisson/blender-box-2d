
import bpy

from .physics_2d_revolute_joint_edit_gizmo import Physics2DRevoluteJointEditGizmo
from .physics_2d_prismatic_joint_edit_gizmo import Physics2DPrismaticJointEditGizmo
from .physics_2d_distance_joint_edit_gizmo import Physics2DDistanceJointEditGizmo
from .physics_2d_wheel_joint_edit_gizmo import Physics2DWheelJointEditGizmo


classes = (
    Physics2DRevoluteJointEditGizmo,
    Physics2DPrismaticJointEditGizmo,
    Physics2DDistanceJointEditGizmo,
    Physics2DWheelJointEditGizmo,
)

def register_joints_groups():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister_joints_groups():
    reverted_classes = reversed(classes)
    for cls in reverted_classes:
        bpy.utils.unregister_class(cls)

    