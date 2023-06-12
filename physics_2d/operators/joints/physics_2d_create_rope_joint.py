
import bpy

from bpy.types import Context, Event
from ...utils import physics_2d_enabled_on_mesh

from .base_joints import Physics2DCreateJointOperator

class Physics2DCreateRopeJointOperator(Physics2DCreateJointOperator):
    """Tooltip"""
    bl_idname = "physics_2d.physics_create_rope_joint"
    bl_label = "Create rope joint"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return physics_2d_enabled_on_mesh(context)
    
    def add_joint(self, context, event):
        return context.scene.three_physics.physics_2d_joints.rope_joints.add()

