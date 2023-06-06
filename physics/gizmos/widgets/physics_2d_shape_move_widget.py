from .physics_2d_move_widget import Physics2DMoveWidget
from ...types import PlanDirection
from ....utils.vertices import create_square_tris_vertices


class Physics2DShapeMoveWidget(Physics2DMoveWidget):
    bl_idname = "VIEW3D_GT_three_physics_2d_shape_move_widget"

    bl_target_properties = (
        {"id": "shape_position", "type": 'FLOAT', "array_length": 2},
    )

    def updateShapes(self):
        self.shapes= list()
        tri_vertices = create_square_tris_vertices()
        self.shapes.append(self.new_custom_shape('TRIS',tri_vertices))