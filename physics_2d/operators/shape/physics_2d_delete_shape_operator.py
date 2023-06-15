import bpy
from bpy.types import Context, Event
from ...utils import physics_2d_enabled_on_mesh


class Physics2DDeleteShapeOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "physics_2d.physics_delete_shape"
    bl_label = "Delete revolute joint"
    bl_options = {'REGISTER', 'UNDO'}

    shape_index: bpy.props.IntProperty(name="Vertex index", default=0)


    @classmethod
    def poll(cls, context):
        return physics_2d_enabled_on_mesh(context)


    def invoke(self, context: Context, event:Event):

        context.object.data.three_rigid_body_2d.shapes.remove(self.shape_index)

        return {'FINISHED'}


    def execute(self, context):



        return {'FINISHED'}