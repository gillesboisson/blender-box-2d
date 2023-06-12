
from ...widgets.physics_2d_square_widget import Physics2DWidget
from bpy.types import Context, Gizmo

from mathutils import Vector
from ...widgets.physics_2d_move_widget import Physics2DMoveWidget
from .....utils.vertices import create_line_vertices


class Physics2DDistanceWidget(Physics2DWidget):
    bl_idname = "VIEW3D_GT_physics_2d_distance_widget"

    bl_target_properties = (
        {"id": "anchor_a", "type": 'FLOAT', "array_length": 2},
        {"id": "anchor_b", "type": 'FLOAT', "array_length": 2},
    )
    
    def updateShapes(self):
        self.shapes= list()
        line_rad = 0.2
        line_len = 1
        self.shapes.append(self.new_custom_shape('LINES',create_line_vertices(
            list(((0,-line_rad),(line_len,-line_rad),(0,line_rad),(line_len,line_rad)))
        )))
            
            