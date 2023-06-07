import bpy
from bpy.types import Context, Event
from bpy_extras import view3d_utils
from mathutils import Vector
from .physics_2d_widget import Physics2DWidget
from ...types import PlanDirection
from ....utils.vertices import create_circle_tris_vertices, vec_3_to_tuple_2


import math
from math import pi

pi2 = pi * 2
deg_to_rad = pi / 180
rad_to_deg = 180 / pi


class Physics2DShapeRotateWidget(Physics2DWidget):
    bl_idname = "VIEW3D_GT_three_physics_2d_shape_rotate_widget"

    bl_target_properties = (
        {"id": "shape_angle", "type": 'FLOAT'},
        {"id": "shape_position", "type": 'FLOAT', "array_length": 2},

    )

    def get_local_angle(self, context, position: Vector):

        local_position_2d = vec_3_to_tuple_2(context.scene.three_physics.physics_2d_orientation, position)
        local_position_2d = (local_position_2d[0] - self.shape_init_position[0], local_position_2d[1] - self.shape_init_position[1])




        plan_position_vec_2 = Vector(local_position_2d).normalized()

        local_angle = math.acos(plan_position_vec_2.x)


        if plan_position_vec_2.y < 0:
            local_angle = -local_angle


        return local_angle


    def invoke(self, context, event):
        shape_angle = self.target_get_value("shape_angle")

        self.shape_init_angle = shape_angle * deg_to_rad
        self.shape_init_position =  self.target_get_value("shape_position")


        self.init_mouse(context, event)

        self.mouse_init_angle = self.get_local_angle(context, self.mouse_3d_init_position)


        return {'RUNNING_MODAL'}

    def modal(self, context: Context, event: Event, tweak):
        orientation = context.scene.three_physics.physics_2d_orientation


        if event.type == 'MOUSEMOVE':

            mouse_vec = Vector((event.mouse_region_x, event.mouse_region_y))
            mouse_vec_3d = view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse_vec, Vector((0,0,0)))
            local_mouse_3d = self.get_local_position(context, mouse_vec_3d)

            # angle_mouse_offset = local_mouse_3d_offset - self.mouse_3d_init_position 
            local_mouse_angle = self.get_local_angle(context, local_mouse_3d)



            local_mouse_angle_offset = local_mouse_angle - self.mouse_init_angle

            while(local_mouse_angle_offset >= pi):
                local_mouse_angle_offset -= pi2
            while(local_mouse_angle_offset <= -pi):
                local_mouse_angle_offset += pi2


            if 'SNAP' in tweak:
                # delta = round(delta)
                local_mouse_angle_offset = round(local_mouse_angle_offset / (pi / 4)) * (pi / 4)
            if 'PRECISE' in tweak:
                # delta /= 10.0
                local_mouse_angle_offset = local_mouse_angle_offset / 10.0

            shape_angle = self.shape_init_angle + local_mouse_angle_offset

            shape_angle_deg = shape_angle
            while(shape_angle_deg >= pi):
                shape_angle_deg -= pi2
            while(shape_angle_deg <= -pi):
                shape_angle_deg += pi2

            self.target_set_value("shape_angle",shape_angle_deg * rad_to_deg)

        return {'RUNNING_MODAL'}

    def updateShapes(self):
        self.shapes= list()
        tri_vertices = create_circle_tris_vertices(radius=0.5, position= Vector((5,0)))
        self.shapes.append(self.new_custom_shape('TRIS',tri_vertices))
        self.shapes.append(self.new_custom_shape('LINES',((0,0,0),(5,0,0))))
        

    def exit(self, context: Context, cancel: bool | None):
        if cancel:
            self.target_set_value("shape_angle", self.shape_init_angle * rad_to_deg)
        else :
            bpy.ops.ed.undo_push()