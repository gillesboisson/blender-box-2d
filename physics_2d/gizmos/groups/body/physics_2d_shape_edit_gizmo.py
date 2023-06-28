from math import pi
from mathutils import Matrix, Vector
from .....utils.plan import clamp_matrix_to_plan, get_plan_2d_vector, get_plan_matrix
from ...widgets.physics_2d_shape_move_widget import Physics2DShapeMoveWidget
from ...widgets.physics_2d_shape_rotate_widget import Physics2DShapeRotateWidget

from bpy.types import (Context, GizmoGroup, Operator)
from bpy.props import *

class Physics2DShapeEditGizmo(GizmoGroup):

    last_shapes_len = 0

    def object_inv_scale(self, context: Context,matrix_world ):

        body_world_mat_scale = matrix_world.to_scale()
        inv_scale = Vector((1.0/body_world_mat_scale.x,1.0/body_world_mat_scale.y,1.0/body_world_mat_scale.z))
        scale_2d = get_plan_2d_vector(context.scene.three_physics.physics_2d_orientation, inv_scale)

        

        # inv_scale_mat = Matrix.Scale(inv_scale.x,4,Vector((1.0,0.0,0.0))) @ Matrix.Scale(inv_scale.y,4,Vector((0.0,1.0,0.0))) @ Matrix.Scale(inv_scale.z,4,Vector((0.0,0.0,1.0)))
        # inv_scale_mat @= orientation_mat
        return scale_2d
    
    def object_inv_scale_mat(self, context: Context,matrix_world ):

        inc_scale = self.object_inv_scale(context, matrix_world)

        return Matrix(((inc_scale.x,0,0,0),(0,inc_scale.y,0,0),(0,0,1,0),(0,0,0,1)))
        

    def get_widget_base_matrix(self, context: Context, shape):
       
       

        matrix_world = context.object.matrix_world
        plan_direction = context.scene.three_physics.physics_2d_orientation
        orientation_mat = get_plan_matrix(plan_direction)

      


       
        clamp_world_mat = clamp_matrix_to_plan(plan_direction, matrix_world, True)



        
        local_mat = Matrix.Translation(Vector((shape.shape_position[0],shape.shape_position[1],0.0)))
        
        return clamp_world_mat @ orientation_mat @ local_mat

    
    def setup_widget_colors(self, context: Context):
          # blender orange widget 
        self.transform_widget_color = 0.8, 0.4, 0.0
        self.transform_widget_color_highlight = 1.0, 0.5, 0.2
        self.transform_widget_alpha = 0.8
        self.transform_widget_alpha_highlight = 1.0

        # if(context.object.data.three_rigid_body_2d.body_type == 'static'):
        #     self.polygon_widget_color = 0.5, 1.0, 0.5
        #     self.polygon_widget_alpha = 0.8
        # elif(context.object.data.three_rigid_body_2d.body_type == 'dynamic'):
        #     self.polygon_widget_color = 0.5, 0.5, 1.0
        #     self.polygon_widget_alpha = 0.8
        # else:
        #     self.polygon_widget_color = 0.5, 0.5, 0.5
        #     self.polygon_widget_alpha = 0.8

        

    def refresh_shape_widgets(self, context: Context, shape, ind):

        if(len(self.rotate_widgets) <= ind):
            rotate_widget = self.gizmos.new(Physics2DShapeRotateWidget.bl_idname)
            self.rotate_widgets.append(rotate_widget)
            rotate_widget.use_draw_modal = True
            rotate_widget.scale_basis = 0.2
            rotate_widget.color = self.transform_widget_color
            rotate_widget.alpha = self.transform_widget_alpha
            rotate_widget.color_highlight = self.transform_widget_color_highlight
            rotate_widget.alpha_highlight = self.transform_widget_alpha_highlight
        else:
            rotate_widget = self.rotate_widgets[ind]

        rotate_widget.target_set_prop('shape_angle', shape,"shape_angle")
        rotate_widget.target_set_prop('shape_position', shape,"shape_position")
        rotate_widget.hide = not self.display_shape_gizmos

        if(len(self.move_widgets) <= ind):
            move_widget = self.gizmos.new(Physics2DShapeMoveWidget.bl_idname)
            self.move_widgets.append(move_widget)
            move_widget.use_draw_modal = True
            move_widget.scale_basis = 0.4
            move_widget.color = self.transform_widget_color
            move_widget.alpha = self.transform_widget_alpha
            move_widget.color_highlight = self.transform_widget_color_highlight
            move_widget.alpha_highlight = self.transform_widget_alpha_highlight

        else:
            move_widget = self.move_widgets[ind]

        move_widget.target_set_prop('shape_position', shape,"shape_position")
        move_widget.hide = not self.display_shape_gizmos

        # if(len(self.polygon_widgets) <= ind):
        #     polygon_widget = self.gizmos.new(self.poly_gizmo_bl_name)
        #     self.polygon_widgets.append(polygon_widget)
        #     polygon_widget.use_draw_scale = False
        #     polygon_widget.hide = True
        # else:
        #     polygon_widget = self.polygon_widgets[ind]

        # polygon_widget.target_set_prop("body_type", context.object.data.three_rigid_body_2d, "body_type")
        # polygon_widget.target_set_prop("display_shape_gizmos", context.scene.three_physics.physics_2d_viewport_settings, "display_shape_gizmos")
        

        # polygon_widget.color = self.polygon_widget_color
        # polygon_widget.alpha = self.polygon_widget_alpha
        # polygon_widget.color_highlight  = self.polygon_widget_color
        # polygon_widget.alpha_highlight = self.polygon_widget_alpha

    def refresh_shapes_widgets(self, context: Context):
        self.display_shape_gizmos = context.scene.three_physics.physics_2d_viewport_settings.display_shape_gizmos
        
        ind = 0
        for ind_shape in range(len(context.object.data.three_rigid_body_2d.shapes)):
            shape = context.object.data.three_rigid_body_2d.shapes[ind_shape]
            if shape.shape_type == self.shape_type:
                self.refresh_shape_widgets(context, context.object.data.three_rigid_body_2d.shapes[ind_shape], ind)
                ind += 1
        
        len_shapes = ind
        len_widgets = len(self.rotate_widgets)
        
        self.remove_shapes_widgets(context, len_shapes, len_widgets)


    def remove_shapes_widgets(self, context: Context, len_shapes, len_widgets):
            for(ind_del) in range(len_shapes, len_widgets):
                self.remove_shape_widget(len_shapes)
 

    def remove_shape_widget(self, ind_shape):
        rotate_gizmo = self.rotate_widgets[ind_shape]
        self.gizmos.remove(rotate_gizmo)
        self.rotate_widgets.remove(rotate_gizmo)

        move_gizmo = self.move_widgets[ind_shape]
        self.gizmos.remove(move_gizmo)
        self.move_widgets.remove(move_gizmo)

        

    def setup(self, context: Context):        
        
        self.setup_widget_colors(context)

        self.rotate_widgets = list()
        self.move_widgets = list()
        self.polygon_widgets = list() 

        self.refresh_shapes_widgets(context)


    def refresh(self, context: Context):
        self.setup_widget_colors(context)
        self.refresh_shapes_widgets(context)

    def draw_prepare(self, context: Context):
        last_shapes_len = len(context.object.data.three_rigid_body_2d.shapes)
        if(self.last_shapes_len != last_shapes_len):
            self.refresh_shapes_widgets(context)
            self.last_shapes_len = last_shapes_len

        self.refresh_shape_mats(context)

    def scale_mat(self, context: Context, shape, ind_shape):
        return Matrix()

    def refresh_shape_mat(self, context: Context,base_mat, local_mat,  shape, ind_shape):
        rotate_widget = self.rotate_widgets[ind_shape]
        move_widget = self.move_widgets[ind_shape]
        # polygon_widget = self.polygon_widgets[ind_shape]


        move_widget.matrix_basis = local_mat @ self.cached_object_inv_scale_mat
        rotate_widget.matrix_basis =  local_mat @ self.cached_object_inv_scale_mat
        # polygon_widget.matrix_basis =  local_mat @ self.scale_mat(context,shape,ind_shape) @ inv_mat

    def refresh_shape_mats(self, context: Context):
        ind = 0

        # pre computed object inverted scale mat in physics 2d plan in order to keep widget size constant
        # as object scale still need transform widget position but not the widget handle
        # this mat is used in refresh_shape_mat at the very and of widget transformation

        self.cached_object_inv_scale_mat = self.object_inv_scale_mat(context, context.object.matrix_world)    
        for ind_shape in range(len(context.object.data.three_rigid_body_2d.shapes)):
            shape = context.object.data.three_rigid_body_2d.shapes[ind_shape]
            if shape.shape_type == self.shape_type and ind < len(self.rotate_widgets):
                base_mat = self.get_widget_base_matrix(context, shape) 
                local_mat = base_mat @ Matrix.Rotation(shape.shape_angle * pi / 180.0, 4, 'Z') 
                self.refresh_shape_mat(context, base_mat,local_mat, context.object.data.three_rigid_body_2d.shapes[ind_shape], ind)
                ind += 1

