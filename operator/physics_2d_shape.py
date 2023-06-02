import bpy
from mathutils import Matrix
from ..utils.shader_helpers import drawPolyline, drawPolyline2D
from ..utils.vertices import create_polygon_vertices, vec_2_to_vec_3


def addVertexToShape(context):
    context.active_object.data.three_rigid_body_2d.shape.shape_polygon_vertices.add()
        
def removeVertexToShape(context, index):
    context.active_object.data.three_rigid_body_2d.shape.shape_polygon_vertices.remove(index)






class AddVertexToPolygonShapeOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "physics_2d.add_shape_vertex"
    bl_label = "Add shape vertex"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.data.three_rigid_body_2d and context.active_object.data.three_rigid_body_2d.enabled and context.active_object.data.three_rigid_body_2d.shape.shape_type == 'polygon'

    def execute(self, context):
        addVertexToShape(context)
        return {'FINISHED'}




class RemoveVertexToPolygonShapeOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "physics_2d.remove_shape_vertex"
    bl_label = "Remove shape vertex"

    vertex_index: bpy.props.IntProperty(name="Vertex index", default=0)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.data.three_rigid_body_2d and context.active_object.data.three_rigid_body_2d.enabled and context.active_object.data.three_rigid_body_2d.shape.shape_type == 'polygon'

    def execute(self, context):
        removeVertexToShape(context, self.vertex_index)
        return {'FINISHED'}


from gpu_extras.batch import batch_for_shader
import gpu

shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')

def draw_vertices(self, context):


    polygon_vertices = context.active_object.data.three_rigid_body_2d.shape.shape_polygon_vertices
    vertices2D = list()

    for ind in range(len(polygon_vertices)):
        if(ind == self.vertex_index):
            vertices2D.append((self.editedVertex.pos[0],self.editedVertex.pos[1]))
        else:
            vertices2D.append((polygon_vertices[ind].pos[0],polygon_vertices[ind].pos[1]))

    # vertices = create_polygon_vertices(vertices2D, context.scene.three_physics.physics_2d_orientation)
    
    # drawPolyline(vertices, (1,1,0,1), self.mat)
    drawPolyline2D(vertices2D, (1,1,0,1), self.mat)


class EditPolygon2DVertexOperator(bpy.types.Operator):
    bl_idname = "physics_2d.edit_shape_vertex"
    bl_label = "Edit shape vertex"
    vertex_index: bpy.props.IntProperty(name="Vertex index", default=0)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.data.three_rigid_body_2d and context.active_object.data.three_rigid_body_2d.enabled and context.active_object.data.three_rigid_body_2d.shape.shape_type == 'polygon'


    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type == 'MOUSEMOVE':
            # self.mouse_path.append((event.mouse_region_x, event.mouse_region_y))
            print(event.mouse_region_x, event.mouse_region_y)
        elif event.type == 'LEFTMOUSE':
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            
            self.editedVertex =  context.active_object.data.three_rigid_body_2d.shape.shape_polygon_vertices[self.vertex_index]
            pos2D = context.active_object.data.three_rigid_body_2d.shape.shape_position
            orientation = context.scene.three_physics.physics_2d_orientation
            self.shape_position  = vec_2_to_vec_3(orientation ,pos2D) 

            args = (self, context)
            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_vertices, args, 'WINDOW', 'POST_VIEW')
            self.mat = context.active_object.matrix_world.copy()
            self.mat @= Matrix.Translation(self.shape_position)
            
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}