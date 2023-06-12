
from ...widgets.physics_2d_square_widget import Physics2DWidget
from bpy.types import Context, Gizmo

from mathutils import Vector
from .....utils.vertices import create_line_vertices


class Physics2DAxeWidget(Physics2DWidget):
    bl_idname = "VIEW3D_GT_physics_2d_axe_widget"

    bl_target_properties = (
        {"id": "direction", "type": 'FLOAT', "array_length": 2},
    )


    def updateShapes(self):
        self.shapes = list()
        self.shapes.append(self.new_custom_shape('LINES', create_line_vertices(list(((0,0),(1,0))))))
    

