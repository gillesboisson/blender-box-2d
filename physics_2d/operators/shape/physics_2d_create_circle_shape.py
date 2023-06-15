

from bpy.types import Context
from ...utils import physics_2d_enabled_on_mesh

from bpy.types import Context, Operator

class Physics2DCreateCircleShapeOperator(Operator):
    """Tooltip"""
    bl_idname = "physics_2d.physics_create_circle_shape"
    bl_label = "Create circle shape"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return physics_2d_enabled_on_mesh(context)
    
    
    
    def invoke(self, context: Context, event):
        shape = context.object.data.three_rigid_body_2d.shapes.add()
        shape.shape_type = 'circle'

        return {'FINISHED'}