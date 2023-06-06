from bpy.types import Gizmo
from bpy_extras import view3d_utils
from mathutils import Vector
from ...types import PlanDirection
from ....utils.plan import clamp_matrix_to_plan


class Physics2DWidget(Gizmo):

    shapes = list()

    last_orientation = None

    mouse_3d_offset = Vector((0,0,0))


    # def update_orientation(self, context):
    #     orientation = context.scene.three_physics.physics_2d_orientation

    #     if self.last_orientation != orientation:
    #         self.updateShapes()
    #         self.last_orientation = orientation

        # self.update_mat( context)

    def draw(self, context):
        # self.update_orientation(context)

        for shape in self.shapes:
            self.draw_custom_shape(shape)

    def draw_select(self, context, select_id):
        # self.update_orientation(context)

        for shape in self.shapes:
            self.draw_custom_shape(shape, select_id = select_id)

    def updateShapes(self):
        return

    def setup(self):
        self.updateShapes()
        return

    def get_local_position(self, context, position):
        face_direction = context.scene.three_physics.physics_2d_orientation
        object_local_matrix = clamp_matrix_to_plan(face_direction, context.object.matrix_world).inverted()
        # position_3d = vec_2_to_vec_3(orientation, position)

        return object_local_matrix @ position



    def init_mouse(self, context, event):
        mouse_vec = Vector((event.mouse_region_x, event.mouse_region_y))
        mouse_position_3d = view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse_vec, Vector((0,0,0)))

        self.mouse_3d_init_position = self.get_local_position(context, mouse_position_3d)

    def get_local_mouse_offset(self, context, event):
        mouse_vec = Vector((event.mouse_region_x, event.mouse_region_y))
        mouse_3d = view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse_vec, Vector((0,0,0)))
        return self.get_local_position(context, mouse_3d)