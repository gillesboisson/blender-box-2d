
import bpy

from bpy.types import Context, Event
from ...utils import physics_2d_enabled_on_mesh
from ....utils.plan import get_plan_matrix

from .base_joints import Physics2DCreateJointOperator

class Physics2DCreateWheelJointOperator(Physics2DCreateJointOperator):
    """Tooltip"""
    bl_idname = "physics_2d.physics_create_wheel_joint"
    bl_label = "Create wheel joint"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return physics_2d_enabled_on_mesh(context)
    
    def add_joint(self, context, event):
        return context.scene.three_physics.physics_2d_joints.wheel_joints.add()

    def set_joint_props(self, context, joint, body_a, body_b):
        plan_direction = context.scene.three_physics.physics_2d_orientation
        orientation_mat = get_plan_matrix(plan_direction).inverted()
        local_position_a = orientation_mat @ body_a.matrix_world.translation
        local_position_b = orientation_mat @ body_b.matrix_world.translation
        len = (local_position_a - local_position_b).length
        joint.length = len
        return