
from bpy.types import Context, Gizmo

from mathutils import Vector
from ...widgets.physics_2d_move_widget import Physics2DMoveWidget
from .....utils.vertices import create_arrow_line_vertices


class Physics2DPrismaticAxeWidget(Gizmo):
    bl_idname = "VIEW3D_GT_physics_2d_prismatic_axe_widget"

    bl_target_properties = (
        {"id": "direction", "type": 'FLOAT', "array_length": 2},
    )


    def setup(self):
        self.shape = self.new_custom_shape('LINES', create_arrow_line_vertices(length=50, offset=Vector((-25,0)), header_size=Vector((0.5,0.5))))
    

    def draw(self, context):
        self.draw_custom_shape(self.shape)


    def draw_select(self, context, select_id):
        self.draw_custom_shape(self.shape, select_id = select_id)
