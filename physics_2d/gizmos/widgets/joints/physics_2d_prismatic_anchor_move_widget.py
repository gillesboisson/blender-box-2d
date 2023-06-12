from mathutils import Vector
from ...widgets.physics_2d_move_widget import Physics2DMoveWidget
from .....utils.vertices import create_cross_line_vertices, create_square_tris_vertices


class Physics2DPrismaticAnchorMoveWidget(Physics2DMoveWidget):
    bl_idname = "VIEW3D_GT_physics_2d_prismatic_anchor_move_widget"

    bl_target_properties = (
        {"id": "anchor_position", "type": 'FLOAT', "array_length": 2},
        {"id": "display_joint_gizmo", "type": 'BOOLEAN'},

    )

    position_property_name = "anchor_position"

    def updateShapes(self):
        lines = create_cross_line_vertices()
        self.shapes.append(self.new_custom_shape('LINES',create_cross_line_vertices()))
        self.shapes.append(self.new_custom_shape('TRIS',create_square_tris_vertices(size=Vector((0.6,0.6)))))