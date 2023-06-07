import bpy
from .actions import removeVertexToShape


class ThreePhysics2DRemoveVertexToPolygonShapeOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "three_physics_2d.remove_shape_vertex"
    bl_label = "Remove shape vertex"

    vertex_index: bpy.props.IntProperty(name="Vertex index", default=0)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.data.three_rigid_body_2d and context.active_object.data.three_rigid_body_2d.enabled and context.active_object.data.three_rigid_body_2d.shape.shape_type == 'polygon'

    def execute(self, context):
        removeVertexToShape(context, self.vertex_index)
        return {'FINISHED'}