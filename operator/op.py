import bpy

class ThreePhysicsCreateBoxVerticesOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    vertex: bpy.props.FloatVectorProperty(name="Vertex", size=2, default=(0.0, 0.0))

    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'

    def execute(self, context):
        main(context)
        return {'FINISHED'}
    
