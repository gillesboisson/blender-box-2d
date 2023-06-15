from math import pi
from bpy.types import Context, Event
from mathutils import Matrix, Vector

from .physics_2d_widget import Physics2DWidget
from ...types import PlanDirection
from ....utils.vertices import create_circle_tris_vertices, create_square_tris_vertices
from ....utils.plan import clamp_matrix_to_plan, get_plan_matrix



class Physics2DVertexCreateWidget(Physics2DWidget):
    bl_idname = "VIEW3D_GT_physics_2d_vertex_create_widget"

    create_position = Vector((0,0))
    create_ind = -1

    def modal(self, context: Context, event: Event, tweak):
        return {'FINISHED'}

    def invoke(self, context, event):
        print('invoke')
        vertices = self.shape.shape_polygon_vertices
        ind = len(vertices)
        p = vertices.add()
        p.pos = (self.create_position[0],self.create_position[1])
        vertices.move(ind, self.create_ind + 1)
        self.group.refresh_shapes_widgets(context)
        return {'FINISHED'}

    def select_refresh(self):
        print('select_refresh')
        return
        # return super().select_refresh()

    def updateShapes(self):
        self.shapes= list()
        tri_vertices = create_circle_tris_vertices()
        self.shapes.append(self.new_custom_shape('TRIS',tri_vertices))