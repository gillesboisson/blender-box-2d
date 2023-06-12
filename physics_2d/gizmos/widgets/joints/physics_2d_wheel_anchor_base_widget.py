from math import pi

from ..physics_2d_move_widget import Physics2DMoveWidget
from .....utils.vertices import create_circle_line_vertices, create_square_tris_vertices


class Physics2DWheelAnchorBaseMoveWidget(Physics2DMoveWidget):
    bl_idname = "VIEW3D_GT_physics_2d_wheel_anchor_base_move_widget"

    bl_target_properties = (
        {"id": "anchor_position", "type": 'FLOAT', "array_length": 2},
        {"id": "display_joint_gizmo", "type": 'BOOLEAN'},

    )
    
    position_property_name = "anchor_position"
        

    def updateShapes(self):
        self.shapes= list()
        # tri_vertices = create_square_tris_vertices(radius=0.8)
        self.shapes.append(self.new_custom_shape('TRIS',create_square_tris_vertices()))




        

