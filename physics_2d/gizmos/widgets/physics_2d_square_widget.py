from mathutils import Vector
from .physics_2d_widget import Physics2DWidget
from ...types import PlanDirection
from ....utils.vertices import create_square_line_vertices


class Physics2DSquareWidget(Physics2DWidget):

    bl_idname = "VIEW3D_GT_three_physics_2d_square_widget"

    bl_target_properties = (
        {"id": "body_type", "type": 'ENUM'},
        {"id": "display_shape_gizmos", "type": 'BOOLEAN'},
        
    )

    def updateShapes(self):
        self.shapes= list()
        tri_vertices = create_square_line_vertices( size=Vector((1,1)))
        self.shapes.append(self.new_custom_shape('LINES',tri_vertices))