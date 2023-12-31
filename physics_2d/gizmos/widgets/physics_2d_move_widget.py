from time import time
from bpy.types import Context, Event
from mathutils import Matrix
from ...utils import get_snap_from_view_zoom_level
from .physics_2d_widget import Physics2DWidget
from ....utils.vertices import tuple_2_to_vec_3, vec_3_to_tuple_2

import bpy


class Physics2DMoveWidget(Physics2DWidget):

    last_click_time = 0




    move_transform_matrix = Matrix()
    def invoke(self, context, event):
        orientation = context.scene.three_physics.physics_2d_orientation
        self.shape_init_position = self.target_get_value(self.position_property_name)
        position_3d = tuple_2_to_vec_3(orientation, self.shape_init_position)
        self.shape_init_local_position = self.get_local_position(context, position_3d)

        self.init_mouse(context, event)

        self.move_freedom = "XY"

        return {'RUNNING_MODAL'}
    
    
    def is_double_clicking(self, context):
        current_time =  time() * 1000
        current_time_offset = current_time - self.last_click_time
        
        res = False
        if current_time_offset < 300:  # Adjust the time threshold as needed
            res = True
            # Your code here for handling the double click event
        
        self.last_click_time = current_time
        return res
    
    def is_clicking(self, context):
        current_time =  time() * 1000
        current_time_offset = current_time - self.last_click_time
        
        res = False
        if current_time_offset < 300:
            res = True

        return res

    def exit(self, context: Context, cancel: bool | None):
        if cancel:
            self.target_set_value(self.position_property_name, self.shape_init_position)
        else :
            bpy.ops.ed.undo_push()



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

            local_mouse_3d = self.get_local_mouse_offset(context, event)

            

            shape_position_offset_3d = self.move_transform_matrix @ (local_mouse_3d - self.mouse_3d_init_position)
            self.shape_position_offset = vec_3_to_tuple_2(physics_2d_orientation, shape_position_offset_3d) 

            if 'SNAP' in tweak:
                # delta = round(delta)
                snap = get_snap_from_view_zoom_level(context)  
                self.shape_position_offset = (round(self.shape_position_offset[0] / snap) * snap, round(self.shape_position_offset[1]/ snap) * snap)
            if 'PRECISE' in tweak:
                # delta /= 10.0
                self.shape_position_offset = (self.shape_position_offset[0] / 10.0, self.shape_position_offset[1] / 10.0)
            refresh = True

        if refresh:

            shape_position = (self.shape_init_position[0], self.shape_init_position[1])

            if self.move_freedom == "XY" or self.move_freedom == "X":
                shape_position = (shape_position[0] + self.shape_position_offset[0], shape_position[1])
            if self.move_freedom == "XY" or self.move_freedom == "Y":
                shape_position = (shape_position[0], shape_position[1] + self.shape_position_offset[1])



            self.target_set_value(self.position_property_name, shape_position)



        return {'RUNNING_MODAL'}