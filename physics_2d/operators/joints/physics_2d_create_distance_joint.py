
import bpy

from bpy.types import Context, Event
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
    
    def add_joint(self, context, event):
        return context.scene.three_physics.physics_2d_joints.distance_joints.add()

