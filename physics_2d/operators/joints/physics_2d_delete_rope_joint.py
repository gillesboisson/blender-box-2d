
import bpy

from bpy.types import Context, Event
from ...utils import physics_2d_enabled

class Physics2DDeleteRopeJointOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "physics_2d.physics_delete_rope_joint"
    bl_label = "Delete rope joint"
    bl_options = {'REGISTER', 'UNDO'}

    joint_index: bpy.props.IntProperty(name="Vertex index", default=0)
    
    @classmethod
    def poll(cls, context):
        return physics_2d_enabled(context)
    

    def invoke(self, context: Context, event:Event):

        
        context.scene.three_physics.physics_2d_joints.rope_joints.remove(self.joint_index)


        return {'FINISHED'}
    

    def execute(self, context):



        return {'FINISHED'}