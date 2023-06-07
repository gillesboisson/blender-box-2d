from bpy.types import Context, Event
from mathutils import Matrix
from .physics_2d_widget import Physics2DWidget
from ....utils.vertices import tuple_2_to_vec_3, vec_3_to_tuple_2


class Physics2DMoveWidget(Physics2DWidget):
    move_transform_matrix = Matrix()
    def invoke(self, context, event):

        orientation = context.scene.three_physics.physics_2d_orientation
        self.shape_init_position = self.target_get_value(self.position_property_name)
        position_3d = tuple_2_to_vec_3(orientation, self.shape_init_position)
        self.shape_init_local_position = self.get_local_position(context, position_3d)

        self.init_mouse(context, event)

        self.move_freedom = "XY"


        return {'RUNNING_MODAL'}

    def exit(self, context: Context, cancel: bool | None):
        if cancel:
            self.target_set_value(self.position_property_name, self.shape_init_position)




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
                self.shape_position_offset = (round(self.shape_position_offset[0]), round(self.shape_position_offset[1]))
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