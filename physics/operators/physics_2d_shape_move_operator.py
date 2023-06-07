
from bpy_extras import view3d_utils
from mathutils import Matrix, Vector

from ..utils import physics_2d_enabled_on_mesh
from ...utils.plan import clamp_matrix_to_plan
from ...utils.vertices import tuple_2_to_vec_3, vec_3_to_tuple_2

import bpy
from bpy.props import *

class Physics2DShapeMoveOperator(bpy.types.Operator):
    """Tooltip""" 
    bl_idname = "physics_2d.shape_move_operator"
    bl_label = "Move physics 2D shape"
    bl_options = {'REGISTER', 'UNDO'}

    shape_position: FloatVectorProperty(name="Shape position", size=2, default=(0,0))
    
    @classmethod
    def poll(cls, context):
        return physics_2d_enabled_on_mesh(context)

    def get_object_matrix_inverted(self, context, face_direction):
        return clamp_matrix_to_plan(face_direction, context.object.matrix_world).inverted()
        

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
     
    def set_move_transform_matrix(self):
        self.move_transform_matrix = Matrix()

    def invoke(self, context, event):

        if context.area.type == 'VIEW_3D':
            print("invoke operator")
            orientation = context.scene.three_physics.physics_2d_orientation
            self.set_move_transform_matrix()
            # self.shape_init_position = context.object.data.three_rigid_body_2d.shape.shape_position
            self.shape_position = context.object.data.three_rigid_body_2d.shape.shape_position
            self.shape_init_position = self.shape_position
            position_3d = tuple_2_to_vec_3(orientation, self.shape_init_position)
            self.shape_init_local_position = self.get_local_position(context, position_3d)
            self.init_mouse(context, event)

            self.move_freedom = "XY"
            
            context.window_manager.modal_handler_add(self)
            return {"RUNNING_MODAL"}
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}
        
    def execute(self, context):
        context.object.data.three_rigid_body_2d.shape.shape_position = self.shape_position

    def modal(self, context, event):
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

            # print(self.shape_position_offset)

            # if 'SNAP' in tweak:
            #     # delta = round(delta)
            #     self.shape_position_offset = (round(self.shape_position_offset[0]), round(self.shape_position_offset[1]))
            # if 'PRECISE' in tweak:
            #     # delta /= 10.0
            #     self.shape_position_offset = (self.shape_position_offset[0] / 10.0, self.shape_position_offset[1] / 10.0)
            refresh = True

        if refresh:

            shape_position = (self.shape_init_position[0], self.shape_init_position[1])

            # print(shape_position)

            if self.move_freedom == "XY" or self.move_freedom == "X":
                shape_position = (shape_position[0] + self.shape_position_offset[0], shape_position[1])
            if self.move_freedom == "XY" or self.move_freedom == "Y":
                shape_position = (shape_position[0], shape_position[1] + self.shape_position_offset[1])


            self.execute(context)
            # self.target_set_value(self.position_property_name, shape_position)
            self.shape_position = shape_position
        
        if event.type == 'LEFTMOUSE':
            return {'FINISHED'}
        
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}

        return {"RUNNING_MODAL"}
    
    def exit(self, context, cancel):
        print("exit")
        if cancel:
            context.object.data.three_rigid_body_2d.shape.shape_position = self.shape_init_position