import typing
from bpy.types import Context, Gizmo
from bpy_extras import view3d_utils
from mathutils import Vector
from ...types import PlanDirection
from ....utils.plan import clamp_matrix_to_plan


class Physics2DWidget(Gizmo):

    shapes = list()

    last_orientation = None

    mouse_3d_offset = Vector((0,0,0))

    reference_object = None
    
    def draw(self, context):

        for shape in self.shapes:
            self.draw_custom_shape(shape)

    def draw_select(self, context, select_id):
        # print("draw_select", select_id)
        for shape in self.shapes:
            self.draw_custom_shape(shape, select_id = select_id)

    def test_select(self, context: Context, location) -> int:
        print("test_select")
        # for shape in self.shapes:
        #     if(self.test_select_custom_shape(context, shape, location)):
        #         return shape.select_id

        return -1

    def updateShapes(self):
        return

    def setup(self):
        self.updateShapes()
        return

    def get_object_matrix_inverted(self, context, face_direction):
        if(self.reference_object is not None):
            ref_object = self.reference_object
        else:
            ref_object = context.object
        return clamp_matrix_to_plan(face_direction, ref_object.matrix_world).inverted()
        

    def get_local_position(self, context, position):
        face_direction = context.scene.three_physics.physics_2d_orientation
        object_local_matrix = self.get_object_matrix_inverted(context, face_direction)
        
        return object_local_matrix @ position



    def init_mouse(self, context, event):
        mouse_vec = Vector((event.mouse_region_x, event.mouse_region_y))
        mouse_position_3d = view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse_vec, Vector((0,0,0)))

        self.mouse_3d_init_position = self.get_local_position(context, mouse_position_3d)

    def get_local_mouse_offset(self, context, event):
        mouse_vec = Vector((event.mouse_region_x, event.mouse_region_y))
        mouse_3d = view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse_vec, Vector((0,0,0)))
        return self.get_local_position(context, mouse_3d)