
import bpy

from bpy.types import Context, Event
from ...utils import physics_2d_enabled

class Physics2DDeleteDistanceJointOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "physics_2d.physics_delete_distance_joint"
    bl_label = "Delete distance joint"
    bl_options = {'REGISTER', 'UNDO'}

    joint_index: bpy.props.IntProperty(name="Vertex index", default=0)
    
    @classmethod
    def poll(cls, context):
        return physics_2d_enabled(context)
    

    def invoke(self, context: Context, event:Event):

        
        context.object.physics_2d_joints.distance_joints.remove(self.joint_index)


        return {'FINISHED'}
    

    def execute(self, context):



        return {'FINISHED'}