from math import pi

from ..physics_2d_move_widget import Physics2DMoveWidget
from .....utils.vertices import create_circle_line_vertices, create_circle_tris_vertices

def anchor_vertices():
    vertices = create_circle_tris_vertices(radius=0.3)
    vertices.extend(create_circle_line_vertices(radius=0.5,end_angle=-3/8 * pi,start_angle= 1/8 * pi))
    return vertices

class Physics2DRevoluteAnchorMoveWidget(Physics2DMoveWidget):
    bl_idname = "VIEW3D_GT_physics_2d_revolute_anchor_move_widget"

    bl_target_properties = (
        {"id": "anchor_position", "type": 'FLOAT', "array_length": 2},
        {"id": "display_joint_gizmo", "type": 'BOOLEAN'},

    )
    
    position_property_name = "anchor_position"
        

    def updateShapes(self):
        self.shapes= list()
        # tri_vertices = create_circle_tris_vertices(radius=0.8)
        self.shapes.append(self.new_custom_shape('TRIS',create_circle_tris_vertices(radius=0.4)))
        # line_vertices = create_circle_line_vertices()
        self.shapes.append(self.new_custom_shape('LINES',create_circle_line_vertices(radius=0.6,end_angle=3 / 2 * pi,start_angle=  pi / 2)))



        

