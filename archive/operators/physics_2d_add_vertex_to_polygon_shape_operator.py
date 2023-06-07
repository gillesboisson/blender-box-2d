import bpy

from .actions import addVertexToShape

class ThreePhysics2DAddVertexToPolygonShapeOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "physics_2d.add_shape_vertex_to_polygon"
    bl_label = "Add shape vertex"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.data.three_rigid_body_2d and context.active_object.data.three_rigid_body_2d.enabled and context.active_object.data.three_rigid_body_2d.shape.shape_type == 'polygon'

    def execute(self, context):
        addVertexToShape(context)
        return {'FINISHED'}