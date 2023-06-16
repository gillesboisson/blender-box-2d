
from math import pi
from mathutils import Matrix, Vector
from .....utils.plan import clamp_matrix_to_plan, get_plan_matrix
import bpy

from bpy.types import (Context, GizmoGroup)
from bpy.props import *
from ....utils import display_shape, physics_2d_enabled 

from .....utils.draw import draw_lines, draw_tris

from .....utils.vertices import create_square_tris_vertices, create_circle_tris_vertices,create_square_line_vertices, create_circle_line_vertices, create_polygon_line_vertices


# draw_shapes_handle = bpy.types.SpaceView3D.draw_handler_add(draw_shapes, args, 'WINDOW', 'POST_PIXEL')

def draw_shapes(self, context):
    # global Physics2DShapeDisplayGizmo_draw_handler
    # context.space_data.draw_handler_remove(Physics2DShapeDisplayGizmo_draw_handler, 'WINDOW')
    if(hasattr(context,'scene') and  physics_2d_enabled(context) and display_shape(context)):
        plan_direction = context.scene.three_physics.physics_2d_orientation
        orientation_mat = get_plan_matrix(plan_direction)

        square = create_square_tris_vertices(plan_direction=plan_direction)
        circle = create_circle_tris_vertices(plan_direction=plan_direction)

        square_outline = create_square_line_vertices(plan_direction=plan_direction)
        circle_outline = create_circle_line_vertices(plan_direction=plan_direction)


        # print('> draws_shapes')
        circle_tuples = list()
        circle_outline_tuples = list()
        for c in circle:
            circle_tuples.append((c.x,c.y,c.z))
        for c in circle_outline:
            circle_outline_tuples.append((c.x,c.y,c.z))

        
        square_tuples = list()
        square_outline_tuples = list()
        
        for c in square:
            square_tuples.append((c.x,c.y,c.z))
        for c in square_outline:
            square_outline_tuples.append((c.x,c.y,c.z))



        for ob in context.scene.objects:
            if ob.type == "MESH" and ob.data != None and ob.data.three_rigid_body_2d != None and ob.data.three_rigid_body_2d.enabled == True:
                shapes = ob.data.three_rigid_body_2d.shapes
                is_selected = ob in context.selected_objects

                if is_selected:
                    shape_color = list((0.4,0.4,0.4,0))
                else:
                    shape_color = list((0.1,0.1,0.1,0))
                    
                if ob.data.three_rigid_body_2d.body_type == 'static':
                    shape_color[1] += 0.4
                    
                elif ob.data.three_rigid_body_2d.body_type == 'dynamic':
                    shape_color[2] += 0.4
                elif ob.data.three_rigid_body_2d.body_type == 'kinetic':
                    shape_color[0] += 0.4
                    
                shape_outline_color = shape_color.copy()
                shape_outline_color[3] = 1
                
                clamp_world_mat = clamp_matrix_to_plan(plan_direction, ob.matrix_world)
                for shape in shapes:
                    local_mat = Matrix.Translation(Vector((shape.shape_position[0],shape.shape_position[1],0.0))) 
                    local_mat @= Matrix.Rotation(shape.shape_angle * pi / 180.0, 4, 'Z')
                    base_mat = clamp_world_mat @ orientation_mat @ local_mat

                    if shape.shape_type == 'box':
                        scale_mat = Matrix.Scale(shape.shape_box_scale[0], 4, Vector((1,0,0))) @ Matrix.Scale(shape.shape_box_scale[1], 4, Vector((0,1,0)))
                        shape_mat = base_mat @ scale_mat
                        if not is_selected:
                            draw_tris(square_tuples, shape_color, shape_mat)
                        draw_lines(square_outline_tuples, shape_outline_color, shape_mat)

                    elif shape.shape_type == 'circle':
                        scale_mat = Matrix.Scale(shape.shape_radius,4,(0,0,1))
                        scale_mat = scale_mat @ Matrix.Scale(shape.shape_radius,4,(0,1,0))
                        scale_mat = scale_mat @ Matrix.Scale(shape.shape_radius,4,(1,0,0))
                        shape_mat = base_mat @ scale_mat
                        if not is_selected:
                            draw_tris(circle_tuples, shape_color, shape_mat)
                        draw_lines(circle_outline_tuples, shape_outline_color, shape_mat)


                    elif shape.shape_type == 'polygon':
                        vertices = list()
                        shape_mat = base_mat
                        for vertex in shape.shape_polygon_vertices:
                            vertices.append(vertex.pos)
                        draw_lines(create_polygon_line_vertices(vertices),  shape_color, shape_mat)
                        



Physics2DShapeDisplayGizmo_draw_handler = None

def clear_physic_2d_shape_draw_handler():
    global Physics2DShapeDisplayGizmo_draw_handler
    if(Physics2DShapeDisplayGizmo_draw_handler is not None):
        bpy.types.SpaceView3D.draw_handler_remove(Physics2DShapeDisplayGizmo_draw_handler, 'WINDOW')
        Physics2DShapeDisplayGizmo_draw_handler = None

class Physics2DShapeDisplayEmptyWidget(bpy.types.Gizmo):

    bl_idname = "VIEW3D_GT_physics_2d_shape_display_gizmo_empty_widget"

    bl_target_properties = (
        {"id": "display_shape", "type": 'BOOLEAN'},
    )


    def draw(self, context):
        pass

class Physics2DShapeDisplayGizmo(GizmoGroup):
    bl_idname = "VIEW3D_GT_physics_2d_shape_display_gizmo"
    bl_label = "Physics 2D Shape display"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'SHOW_MODAL_ALL' , 'PERSISTENT'}


    @classmethod
    def poll(cls, context):
        return physics_2d_enabled(context)
        
    
   

    def setup(self, context: Context):
        gz = self.gizmos.new(Physics2DShapeDisplayEmptyWidget.bl_idname)
        gz.target_set_prop('display_shape', context.scene.three_physics.physics_2d_viewport_settings, "display_shape")

        global Physics2DShapeDisplayGizmo_draw_handler
        clear_physic_2d_shape_draw_handler()
        Physics2DShapeDisplayGizmo_draw_handler = bpy.types.SpaceView3D.draw_handler_add(draw_shapes, (self, context), 'WINDOW', 'POST_VIEW')
    
    def draw_prepare(self, context: Context):
        draw_shapes(self,context)


    # def refresh(self, context: Context):
    #     context.area.tag_redraw()
    # return super().refresh(context)
    # def draw_prepare(self, context: Context):
    #     Physics2DShapeDisplayGizmo_draw_handler = context.space_data.draw_handler_add(draw_shapes, (self, context), 'WINDOW', 'POST_PIXEL')
    #     pass