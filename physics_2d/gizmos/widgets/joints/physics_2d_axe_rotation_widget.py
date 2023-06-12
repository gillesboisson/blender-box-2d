from ..physics_2d_widget import Physics2DWidget
from mathutils import Vector

import bpy
from bpy.types import Context, Event
from bpy_extras import view3d_utils
from mathutils import Vector
from ..physics_2d_widget import Physics2DWidget
from ....types import PlanDirection
from .....utils.vertices import create_circle_tris_vertices, vec_3_to_tuple_2

import math
from math import acos, pi

pi2 = pi * 2
deg_to_rad = pi / 180
rad_to_deg = 180 / pi



class Physics2DAxeRotationWidget(Physics2DWidget):
    bl_idname = "VIEW3D_GT_physics_2d_axe_rotation_widget"

    bl_target_properties = (
        {"id": "axis", "type": 'FLOAT', "array_length": 2},
        {"id": "anchor_position", "type": 'FLOAT', "array_length": 2},

    )


    def get_local_angle(self):
        axis_tupple = self.target_get_value("axis")
        axis = Vector((axis_tupple[0],axis_tupple[1])).normalized()
        local_angle = acos(axis.x)
        if axis.y < 0:
            local_angle = -local_angle


        return local_angle

    def get_local_mouse_angle(self, mouse_position: Vector):
        mouse_angle_axis = Vector((
           mouse_position.x - self.init_position[0], 
            mouse_position.y - self.init_position[1]
            )).normalized()
        
        angle = acos(mouse_angle_axis.x)
        if mouse_angle_axis.y < 0:
            angle = -angle

        return angle

    def invoke(self, context, event):

        self.init_axis = self.target_get_value("axis")
        self.init_angle = self.get_local_angle()
        self.init_position =  self.target_get_value("anchor_position")


        self.init_mouse(context, event)

       
        self.mouse_init_angle = self.get_local_mouse_angle( self.mouse_3d_init_position)


        return {'RUNNING_MODAL'}

    def modal(self, context: Context, event: Event, tweak):
        orientation = context.scene.three_physics.physics_2d_orientation


        if event.type == 'MOUSEMOVE':

            mouse_vec = Vector((event.mouse_region_x, event.mouse_region_y))
            mouse_vec_3d = view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse_vec, Vector((0,0,0)))
            local_mouse_3d = self.get_local_position(context, mouse_vec_3d)

            # angle_mouse_offset = local_mouse_3d_offset - self.mouse_3d_init_position 
            local_mouse_angle = self.get_local_mouse_angle(local_mouse_3d)

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

            shape_angle = self.init_angle + local_mouse_angle_offset

            shape_angle_deg = shape_angle
            while(shape_angle_deg >= pi):
                shape_angle_deg -= pi2
            while(shape_angle_deg <= -pi):
                shape_angle_deg += pi2

            axis = (math.cos(shape_angle), math.sin(shape_angle))

            self.target_set_value("axis",axis)

        return {'RUNNING_MODAL'}

    def updateShapes(self):
        self.shapes= list()
        tri_vertices = create_circle_tris_vertices(radius=0.5, position= Vector((5,0)))
        self.shapes.append(self.new_custom_shape('TRIS',tri_vertices))
        # self.shapes.append(self.new_custom_shape('LINES',((0,0,0),(5,0,0))))
        

    def exit(self, context: Context, cancel: bool | None):
        if cancel:
            self.target_set_value("axis", self.init_axis)
        else :
            bpy.ops.ed.undo_push()
        