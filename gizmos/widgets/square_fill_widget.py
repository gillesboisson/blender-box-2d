import math
from bpy.types import (
    Gizmo,
)

from ...physics.types import PlanDirection

from mathutils import Vector, Matrix


class Physics2DWidget(Gizmo):

    shapes = list()

    def draw(self, context):
        for shape in self.shapes:
            self.draw_custom_shape(shape)        
    
    def draw_select(self, context, select_id):
        for shape in self.shapes:
            self.draw_custom_shape(shape, select_id = select_id)        

    def updateShapes(self, context, orientation: PlanDirection):
        return


from ...utils.vertices import create_square_line_vertices, create_square_tris_vertices, tuple_2_to_vec_3
class SquareFillWidget(Physics2DWidget):
    bl_idname = "VIEW3D_GT_square_fill_widget"
    
    def updateShapes(self, context, orientation: PlanDirection):
        self.shapes.clear()
        tri_vertices = create_square_tris_vertices(orientation = orientation)
        self.shapes.append(self.new_custom_shape('TRIS',tri_vertices))

