from math import pi
import math
import typing
from bpy.types import (
    Context,
    Event,
    Gizmo,
)
from bpy.props import *
import bpy
from mathutils import Matrix, Vector
from ....utils.plan import clamp_matrix_to_plan

from ...types import PlanDirection
from ....utils.vertices import create_circle_fill_vertices, create_circle_line_vertices, create_square_line_vertices, create_square_tris_vertices, tuple_2_to_vec_3, vec_3_to_tuple_2

from bpy_extras import view3d_utils

class Physics2DWidget(Gizmo):

    shapes = list()

    last_orientation = None

    
    
   
    mouse_3d_offset = Vector((0,0,0))



    def update_orientation(self, context):
        orientation = context.scene.three_physics.physics_2d_orientation

        if self.last_orientation != orientation:
            self.updateShapes(context, orientation)
            self.last_orientation = orientation

        # self.update_mat( context)

    def draw(self, context):
        self.update_orientation(context)

        for shape in self.shapes:
            self.draw_custom_shape(shape) 
    
    def draw_select(self, context, select_id):
        self.update_orientation(context)

        for shape in self.shapes:
            self.draw_custom_shape(shape, select_id = select_id)       

    def updateShapes(self, context, orientation: PlanDirection):
        return

    def setup(self):
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



pi2 = pi * 2
deg_to_rad = pi / 180
rad_to_deg = 180 / pi
    
class ShapeRotateWidget(Physics2DWidget):
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
    
    def updateShapes(self, context, orientation: PlanDirection):
        self.shapes= list()
        tri_vertices = create_circle_fill_vertices(radius=0.5)
        self.shapes.append(self.new_custom_shape('TRIS',tri_vertices))
    
    def exit(self, context: Context, cancel: bool | None):
        if cancel:
            self.target_set_value("shape_angle", self.shape_init_angle * rad_to_deg)

class PhysicsSquareWidget(Physics2DWidget):

    bl_idname = "VIEW3D_GT_three_physics_2d_square_widget"


    def updateShapes(self, context, orientation: PlanDirection):
        self.shapes= list()
        tri_vertices = create_square_line_vertices( size=Vector((1,1)))
        self.shapes.append(self.new_custom_shape('LINES',tri_vertices))


class Physics2DMoveWidget(Physics2DWidget):
    # shape_position: FloatVectorProperty(size=2, default=(0.0, 0.0))

    def invoke(self, context, event):
        
        orientation = context.scene.three_physics.physics_2d_orientation
        self.shape_init_position = self.target_get_value("shape_position")        
        position_3d = tuple_2_to_vec_3(orientation, self.shape_init_position)
        self.shape_init_local_position = self.get_local_position(context, position_3d)

        self.init_mouse(context, event)
        
        self.move_freedom = "XY"


        return {'RUNNING_MODAL'}
    
    def exit(self, context: Context, cancel: bool | None):
        if cancel:
            self.target_set_value("shape_position", self.shape_init_position)  

        
    
    
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
            
            shape_position_offset_3d = local_mouse_3d - self.mouse_3d_init_position
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



            self.target_set_value("shape_position", shape_position)



        return {'RUNNING_MODAL'}


class ShapeMoveWidget(Physics2DMoveWidget):
    bl_idname = "VIEW3D_GT_three_physics_2d_shape_move_widget"
    
    bl_target_properties = (
        {"id": "shape_position", "type": 'FLOAT', "array_length": 2},
    )
    
    def updateShapes(self, context, orientation: PlanDirection):
        self.shapes= list()
        tri_vertices = create_square_tris_vertices()
        self.shapes.append(self.new_custom_shape('TRIS',tri_vertices))


class ShapeScaleWidget(Physics2DWidget):
    bl_idname = "VIEW3D_GT_three_physics_2d_shape_scale_widget"

    bl_target_properties = (
        {"id": "shape_scale", "type": 'FLOAT', "array_length": 2},
        {"id": "shape_position", "type": 'FLOAT', "array_length": 2},
    )

    def get_mouse_distance(self, context, event):
        mouse_vec = Vector((event.mouse_region_x, event.mouse_region_y))
        mouse_position_3d = view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse_vec, Vector((0,0,0)))
        mouse_3d_init_position = self.get_local_position(context, mouse_position_3d)
        mouse_shape_position = vec_3_to_tuple_2(context.scene.three_physics.physics_2d_orientation, mouse_3d_init_position)
        return math.sqrt(mouse_shape_position[0] ** 2 + mouse_shape_position[1] ** 2)

    def invoke(self, context, event):
        self.shape_init_scale = self.target_get_value("shape_scale")

        self.move_freedom = "XY"

        self.mouse_shape_distance = self.get_mouse_distance(context, event)


        
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
            
            mouse_shape_distance = self.get_mouse_distance(context, event)

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




    def updateShapes(self, context, orientation: PlanDirection):
        self.shapes= list()
        tri_vertices = create_square_tris_vertices()
        self.shapes.append(self.new_custom_shape('TRIS',tri_vertices))



classes = (
    ShapeMoveWidget,
    ShapeRotateWidget,
    PhysicsSquareWidget,
    ShapeScaleWidget
)

def register_physic_2d_shape_widgets():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister_physic_2d_shape_widgets():
    for cls in classes:
        bpy.utils.unregister_class(cls)


