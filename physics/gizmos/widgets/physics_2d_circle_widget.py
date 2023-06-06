from .physics_2d_widget import Physics2DWidget
from ...types import PlanDirection
from ....utils.vertices import create_circle_line_vertices


class Physics2DCircleWidget (Physics2DWidget):
    bl_idname = "VIEW3D_GT_three_physics_2d_circle_widget"

    def updateShapes(self):
        self.shapes= list()
        tri_vertices = create_circle_line_vertices(radius=1)
        self.shapes.append(self.new_custom_shape('LINES',tri_vertices))