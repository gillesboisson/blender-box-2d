import bpy
from bpy.types import Context, Event
from bpy_extras import view3d_utils
from mathutils import Vector
from ....utils.plan import tuple_2_to_vec_3
from .physics_2d_widget import Physics2DWidget
from ...types import PlanDirection
from ....utils.vertices import create_square_tris_vertices, vec_3_to_tuple_2


import math


class Physics2DShapeScaleWidget(Physics2DWidget):
    bl_idname = "VIEW3D_GT_three_physics_2d_shape_scale_widget"

    bl_target_properties = (
        {"id": "shape_scale", "type": 'FLOAT', "array_length": 2},
        {"id": "shape_position", "type": 'FLOAT', "array_length": 2},
    )

    def get_mouse_distance(self, context, event, origin = tuple((0,0))):
        mouse_vec = Vector((event.mouse_region_x, event.mouse_region_y))
        origin_position_3d = tuple_2_to_vec_3(context.scene.three_physics.physics_2d_orientation, origin)
        
        mouse_position_3d = view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse_vec, Vector((0,0,0)))
        mouse_3d_init_position = self.get_local_position(context, mouse_position_3d - origin_position_3d)
        mouse_shape_position = vec_3_to_tuple_2(context.scene.three_physics.physics_2d_orientation, mouse_3d_init_position)
        return math.sqrt(mouse_shape_position[0] ** 2 + mouse_shape_position[1] ** 2)

    def invoke(self, context, event):
        self.shape_init_scale = self.target_get_value("shape_scale")

        self.move_freedom = "XY"

        self.mouse_shape_distance = self.get_mouse_distance(context, event, self.target_get_value("shape_position"))



        return {'RUNNING_MODAL'}

    def modal(self, context: Context, event: Event, tweak):
        physics_2d_orientation = context.scene.three_physics.physics_2d_orientation
        refresh = False

        if event.type in {"X"} and event.value == 'PRESS':
            if(self.move_freedom != "X"):
                self.move_freedom = "X"
            else:
                self.move_freedom = "XY"

            refresh = True

        if event.type in {"Y"} and event.value == 'PRESS':
            if(self.move_freedom != "Y"):
                self.move_freedom = "Y"
            else:
                self.move_freedom = "XY"

            refresh = True

        if event.type == 'MOUSEMOVE':

            mouse_shape_distance = self.get_mouse_distance(context, event, self.target_get_value("shape_position"))

            self.scale_offset = mouse_shape_distance - self.mouse_shape_distance

            refresh = True

            # print("mouse_shape_distance", mouse_shape_distance)

        if refresh:
            if 'SNAP' in tweak:
                # delta = round(delta)
                self.scale_offset = round(self.scale_offset)
            if 'PRECISE' in tweak:
                # delta /= 10.0
                self.scale_offset = self.scale_offset / 10.0

            scale_offsec_vec2 = Vector((0,0))

            if self.move_freedom == "XY":
                scale_offsec_vec2 = Vector((self.scale_offset, self.scale_offset))
            elif self.move_freedom == "X":
                scale_offsec_vec2 = Vector((self.scale_offset, 0))
            elif self.move_freedom == "Y":
                scale_offsec_vec2 = Vector((0, self.scale_offset))



            self.target_set_value("shape_scale", (self.shape_init_scale[0] + scale_offsec_vec2.x, self.shape_init_scale[1] + scale_offsec_vec2.y))

        return {'RUNNING_MODAL'}


    def exit(self, context: Context, cancel: bool | None):
        if cancel:
            self.target_set_value("shape_scale", self.shape_init_scale)
        else :
            bpy.ops.ed.undo_push()




    def updateShapes(self):
        self.shapes= list()
        tri_vertices = create_square_tris_vertices()
        self.shapes.append(self.new_custom_shape('TRIS',tri_vertices))