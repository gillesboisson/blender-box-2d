
from math import cos, pi, sin
import math
import bpy

from bpy.types import Context, Event

from mathutils import Matrix, Vector
from bpy_extras import view3d_utils

from ...props.physics_2d_joints_props import Physics2DRevoluteJointPropertyGroup

from ...utils import physics_2d_enabled


from ....utils.draw import draw_polyline_2D





class Physics2DDeleteRevoluteJointOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "physics_2d.physics_delete_revolute_joint"
    bl_label = "Delete revolute joint"
    bl_options = {'REGISTER', 'UNDO'}

    joint_index: bpy.props.IntProperty(name="Vertex index", default=0)
    

    @classmethod
    def poll(cls, context):
        return physics_2d_enabled(context)
    

    def invoke(self, context: Context, event:Event):

        
        context.scene.three_physics.physics_2d_joints.revolute_joints.remove(self.joint_index)


        return {'FINISHED'}
    

    def execute(self, context):



        return {'FINISHED'}