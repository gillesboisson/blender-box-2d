
from math import cos, pi, sin
import math
import bpy

from bpy.types import Context, Event

from mathutils import Matrix, Vector
from bpy_extras import view3d_utils
from ...types import Physics2DBodyShapeType
from ...props.physics_2d_body_props import Vertex2DPropertyGroup
from ....utils.plan import clamp_matrix_to_plan
from ....utils.vertices import create_square_tris_vertices, vec_3_to_tuple_2

from ....utils.vertices import tuple_2_to_vec_3

from ...utils import physics_2d_enabled_on_mesh


from ....utils.draw import draw_polyline_2D


def a_draw_vertices(self, context):
    
    orientation = context.scene.three_physics.physics_2d_orientation
    draw_polyline_2D(self.vertices, (1,1,1,1), orientation, self.shape_mat, True)


class Physics2DCreateShapePolyOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "physics_2d.physics_create_shape_poly"
    bl_label = "Create shape poly"
    bl_options = {'REGISTER', 'UNDO'}

    radius: bpy.props.FloatProperty(name="Radius", default=1, min=0)
    nb_vertices: bpy.props.IntProperty(name="Nb vertices", default=4, min=3, max=100)
    offset_angle: bpy.props.FloatProperty(name="Offset angle", default=0, min=0, max=360)


    shape_mat = Matrix()

    @classmethod
    def poll(cls, context):
        return physics_2d_enabled_on_mesh(context)

    def get_object_matrix_inverted(self, context, face_direction):
        return clamp_matrix_to_plan(face_direction, context.object.matrix_world).inverted()
        

    def get_local_position(self, context, position):
        face_direction = context.scene.three_physics.physics_2d_orientation
        object_local_matrix = self.get_object_matrix_inverted(context, face_direction)
        
        return object_local_matrix @ position
    def get_mouse_distance(self, context, event):
        mouse_vec = Vector((event.mouse_region_x, event.mouse_region_y))
        mouse_position_3d = view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse_vec, Vector((0,0,0)))
        mouse_3d_init_position = self.get_local_position(context, mouse_position_3d)
        mouse_shape_position = vec_3_to_tuple_2(context.scene.three_physics.physics_2d_orientation, mouse_3d_init_position)
        return math.sqrt(mouse_shape_position[0] ** 2 + mouse_shape_position[1] ** 2)
    
    
    def invoke(self, context: Context, event):

        # if context.area.type == 'VIEW_3D':
        self.nb_vertices = 4
        self.radius = 1
        # self.mouse_shape_distance = self.get_mouse_distance(context, event)
        
        # self.update_vertices(context)
        # args = (self, context)  
        # if(hasattr(self, '_handle')):
        #     bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        # self._handle = bpy.types.SpaceView3D.draw_handler_add(a_draw_vertices, args, 'WINDOW', 'POST_VIEW')
        # context.window_manager.modal_handler_add(self)
        # context.area.tag_redraw()
        # context.object.data.
        self.execute(context)

        return {'FINISHED'}
        # else:
        #     self.report({'WARNING'}, "View3D not found, cannot run operator")
        #     return {'CANCELLED'}


    
    def modal(self, context, event):
        # self.execute(context)
        # if event.type in {"LEFT_ARROW"} and event.value == "PRESS" and self.nb_vertices > 3:
        #     self.nb_vertices -= 1
        #     context.area.tag_redraw()
        #     self.update_vertices(context)
        
        # if event.type in {"RIGHT_ARROW"} and event.value == "PRESS":
        #     self.nb_vertices += 1
        #     context.area.tag_redraw()
        #     self.update_vertices(context)


        # if event.type == "MOUSEMOVE":
        #     mouse_shape_distance = self.get_mouse_distance(context, event)

        #     self.scale_offset = mouse_shape_distance - self.mouse_shape_distance

        #     if event.ctrl:
        #         # delta = round(delta)
        #         self.scale_offset = round(self.scale_offset)
        #     if event.shift:
        #         # delta /= 10.0
        #         self.scale_offset = self.scale_offset / 10.0

        #     self.update_vertices(context)  
        #     self.radius = 1 + self.scale_offset
        #     context.area.tag_redraw()
            

        # if event.type in {"LEFTMOUSE"} and event.value == "PRESS":
        #     # self.execute(context)
        #     bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        #     context.area.tag_redraw()
        #     self.execute(context)
        #     return {'FINISHED'}
        
        # if event.type in {"ESC"} and event.value == "PRESS":
        #     bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        #     context.area.tag_redraw()
        #     return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    
    def update_vertices(self, context):

        self.vertices = list()
        rad_angle = self.offset_angle / 180 * pi
        for i in range(self.nb_vertices):
            angle = i / self.nb_vertices * 2 * pi + rad_angle
            self.vertices.append((self.radius * cos(angle), self.radius * sin(angle)))
            # ------------------------------
        

    def execute(self, context):
        # print("execute")

        context.object.data.three_rigid_body_2d.shape.shape_type = "polygon"
        
        self.update_vertices(context)  
               
        ob = context.object.data
        ob.three_rigid_body_2d.shape.shape_polygon_vertices.clear()

        for i in range(self.nb_vertices):
            v = ob.three_rigid_body_2d.shape.shape_polygon_vertices.add()
            v.pos = self.vertices[i]


        return {'FINISHED'}



        