from .physics_2d_widget import Physics2DWidget
from ...types import PlanDirection
from ....utils.vertices import create_circle_line_vertices


class Physics2DCircleWidget (Physics2DWidget):
    bl_idname = "VIEW3D_GT_three_physics_2d_circle_widget"

    bl_target_properties = (
        {"id": "body_type", "type": 'ENUM'},
        {"id": "display_shape_gizmos", "type": 'BOOLEAN'},
        # {"id": "display_shape", "type": 'BOOLEAN'},
    )

    
    
    def updateShapes(self):
        self.shapes= list()
        tri_vertices = create_circle_line_vertices(radius=1)
        self.shapes.append(self.new_custom_shape('LINES',tri_vertices))