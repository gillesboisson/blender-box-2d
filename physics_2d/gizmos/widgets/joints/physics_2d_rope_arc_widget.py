
from math import pi
from ..physics_2d_square_widget import Physics2DWidget
from bpy.types import Context, Gizmo

from mathutils import Vector
from ..physics_2d_move_widget import Physics2DMoveWidget
from .....utils.vertices import create_circle_line_vertices


class Physics2DRopeArcWidget(Physics2DWidget):
    bl_idname = "VIEW3D_GT_physics_2d_rope_arc_widget"

    bl_target_properties = (
        {"id": "anchor_a", "type": 'FLOAT', "array_length": 2},
        {"id": "anchor_b", "type": 'FLOAT', "array_length": 2},
    )
    
    def updateShapes(self):
        self.shapes= list()
        self.shapes.append(self.new_custom_shape('LINES',create_circle_line_vertices(radius=1,start_angle=-pi / 6, end_angle=pi / 6, nb_segment=8)))
            
            