
import bpy

from bpy.types import Context, Event
from mathutils import Matrix
from ....utils.plan import get_plan_matrix
from ...utils import physics_2d_enabled_on_mesh

from .base_joints import Physics2DCreateJointOperator

class Physics2DCreateDistanceJointOperator(Physics2DCreateJointOperator):
    """Tooltip"""
    bl_idname = "physics_2d.physics_create_distance_joint"
    bl_label = "Create distance joint"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return physics_2d_enabled_on_mesh(context)
    
    def add_joint(self, context, body_a, body_b, event):
        joint =  body_a.physics_2d_joints.distance_joints.add()
        return joint

    def set_joint_props(self, context, joint, body_a, body_b):

        plan_direction = context.scene.three_physics.physics_2d_orientation
        orientation_mat = get_plan_matrix(plan_direction).inverted()
        local_position_a = orientation_mat @ body_a.matrix_world.translation
        local_position_b = orientation_mat @ body_b.matrix_world.translation
        len = (local_position_a - local_position_b).length
        joint.enable_limit = True
        joint.lower = len
        joint.upper = len
        
        return