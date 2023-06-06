from bpy.types import Context, Event
from bpy_extras import view3d_utils
from mathutils import Vector
from .physics_2d_widget import Physics2DWidget
from ...types import PlanDirection
from ....utils.vertices import create_square_tris_vertices, vec_3_to_tuple_2


import math


class Physics2DShapeRadiusWidget(Physics2DWidget):
    bl_idname = "VIEW3D_GT_three_physics_2d_shape_radius_widget"

    bl_target_properties = (
        {"id": "shape_circle_radius", "type": 'FLOAT', "array_length": 2},
        {"id": "shape_radius", "type": 'FLOAT'},
    )

    def get_mouse_distance(self, context, event):
        mouse_vec = Vector((event.mouse_region_x, event.mouse_region_y))
        mouse_position_3d = view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse_vec, Vector((0,0,0)))
        mouse_3d_init_position = self.get_local_position(context, mouse_position_3d)
        mouse_shape_position = vec_3_to_tuple_2(context.scene.three_physics.physics_2d_orientation, mouse_3d_init_position)
        return math.sqrt(mouse_shape_position[0] ** 2 + mouse_shape_position[1] ** 2)

    def invoke(self, context, event):
        self.shape_init_radius = self.target_get_value("shape_radius")
        self.mouse_shape_distance = self.get_mouse_distance(context, event)



        return {'RUNNING_MODAL'}

    def modal(self, context: Context, event: Event, tweak):
        # refresh = False


        if event.type == 'MOUSEMOVE':

            mouse_shape_distance = self.get_mouse_distance(context, event)

            self.scale_offset = mouse_shape_distance - self.mouse_shape_distance



            if 'SNAP' in tweak:
                # delta = round(delta)
                self.scale_offset = round(self.scale_offset)
            if 'PRECISE' in tweak:
                # delta /= 10.0
                self.scale_offset = self.scale_offset / 10.0




            self.target_set_value("shape_radius", self.shape_init_radius + self.scale_offset)

        return {'RUNNING_MODAL'}


    def exit(self, context: Context, cancel: bool | None):
        if cancel:
            self.target_set_value("shape_radius", self.shape_init_radius)




    def updateShapes(self):
        self.shapes= list()
        tri_vertices = create_square_tris_vertices()
        self.shapes.append(self.new_custom_shape('TRIS',tri_vertices))