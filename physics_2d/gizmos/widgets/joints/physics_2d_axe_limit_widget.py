
from ..physics_2d_square_widget import Physics2DWidget
from bpy.types import Context, Gizmo

from mathutils import Vector
from .....utils.vertices import create_line_vertices


class Physics2DAxeLimitWidget(Physics2DWidget):
    bl_idname = "VIEW3D_GT_physics_2d_axe_limit_widget"

    bl_target_properties = (
        {"id": "direction", "type": 'FLOAT', "array_length": 2},
        {"id": "display_joint_gizmos", "type": 'BOOLEAN'},
        {"id": "enable_limit", "type": 'BOOLEAN'},
        {"id": "lower", "type": 'FLOAT'},
        {"id": "upper", "type": 'FLOAT'},

    )


    def updateShapes(self):
        self.shapes = list()
        self.shapes.append(self.new_custom_shape('LINES', create_line_vertices(list(
            ((0,-0.5),(0,0.5),
            (1,-0.5),(1,0.5),
            (0,0),(1,0))
        ))))
    

