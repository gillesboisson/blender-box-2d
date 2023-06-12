from math import pi
from bpy.types import Context, Event
from mathutils import Matrix, Vector

from .physics_2d_move_widget import Physics2DMoveWidget
from ...types import PlanDirection
from ....utils.vertices import create_circle_tris_vertices, create_square_tris_vertices
from ....utils.plan import clamp_matrix_to_plan, get_plan_matrix


class Physics2DVertexMoveWidget(Physics2DMoveWidget):
    bl_idname = "VIEW3D_GT_physics_2d_vertex_move_widget"

    bl_target_properties = (
        {"id": "vertex_position", "type": 'FLOAT', "array_length": 2},
    )

    position_property_name = "vertex_position"

    edit_ind = -1

    def invoke(self, context, event):

        if event.type == 'LEFTMOUSE':
            if self.is_double_clicking(context):
                vertices = context.active_object.data.three_rigid_body_2d.shape.shape_polygon_vertices
                vertices.remove(self.edit_ind) 
                self.group.update_vertex_widgets(context)
                return {'FINISHED'}
            

        return super().invoke(context, event)


    def modal(self, context: Context, event: Event, tweak):
        
        orientation = context.scene.three_physics.physics_2d_orientation
        shape_angle = context.object.data.three_rigid_body_2d.shape.shape_angle

        rotation_mat = Matrix.Rotation(shape_angle / 180 * pi, 4, orientation).inverted()

        self.move_transform_matrix = rotation_mat

        return super().modal(context, event, tweak)

    def updateShapes(self):
        self.shapes= list()
        tri_vertices = create_circle_tris_vertices()
        self.shapes.append(self.new_custom_shape('TRIS',tri_vertices))