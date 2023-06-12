


from math import pi
from mathutils import Matrix, Vector
from ....utils.plan import clamp_matrix_to_plan, get_plan_matrix
from ..widgets.physics_2d_shape_move_widget import Physics2DShapeMoveWidget
from ..widgets.physics_2d_shape_rotate_widget import Physics2DShapeRotateWidget

from bpy.types import (Context, GizmoGroup, Operator)
from bpy.props import *

class Physics2DEditGizmo(GizmoGroup):

    def get_widget_base_matrix(self, context: Context):
        shape = context.object.data.three_rigid_body_2d.shape
        matrix_world = context.object.matrix_world
        plan_direction = context.scene.three_physics.physics_2d_orientation

        # create box scale matrix
        orientation_mat = get_plan_matrix(plan_direction)
        clamp_world_mat = clamp_matrix_to_plan(plan_direction, matrix_world)
        
        local_mat = Matrix.Translation(Vector((shape.shape_position[0],shape.shape_position[1],0.0)))
        # local_mat @= Matrix.Rotation(shape.shape_angle * pi / 180.0, 4, 'Z')
        # scale_mat = Matrix.Scale(shape.shape_box_scale[0],4,(1,0,0)) @ Matrix.Scale(shape.shape_box_scale[1],4,(0,1,0)) 
        
        return clamp_world_mat @ orientation_mat @ local_mat

    def get_shape_widget_color_alpha(self, context: Context):
        if(context.object.data.three_rigid_body_2d.body_type == 'static'):
            widget_color = 0.5, 1.0, 0.5
            widget_alpha = 0.8
        elif(context.object.data.three_rigid_body_2d.body_type == 'dynamic'):
            widget_color = 0.5, 0.5, 1.0
            widget_alpha = 0.8

        else:
            widget_color = 0.5, 0.5, 0.5
            widget_alpha = 0.8

        return widget_color, widget_alpha
    def setup_transform_widget_colors(self, context: Context):
          # blender orange widget 
        self.transform_widget_color = 0.8, 0.4, 0.0
        self.transform_widget_color_highlight = 1.0, 0.5, 0.2
        self.transform_widget_alpha = 0.8
        self.transform_widget_alpha_highlight = 1.0

    
    def refresh_gizmos_target(self, context):
        self.rotate_gizmo.target_set_prop('shape_angle', context.object.data.three_rigid_body_2d.shape,"shape_angle")
        self.rotate_gizmo.target_set_prop('shape_position', context.object.data.three_rigid_body_2d.shape,"shape_position")
        self.move_gizmo.target_set_prop('shape_position', context.object.data.three_rigid_body_2d.shape,"shape_position")
        self.polygon_widget.target_set_prop("body_type", context.object.data.three_rigid_body_2d, "body_type")
        self.polygon_widget.target_set_prop("display_shape_gizmos", context.scene.three_physics.physics_2d_viewport_settings, "display_shape_gizmos")
        
        display_shape_gizmos = context.scene.three_physics.physics_2d_viewport_settings.display_shape_gizmos
        self.rotate_gizmo.hide = not display_shape_gizmos
        self.move_gizmo.hide = not display_shape_gizmos
        


    def setup(self, context: Context):        
        
        self.setup_transform_widget_colors(context)

        self.rotate_gizmo = self.gizmos.new(Physics2DShapeRotateWidget.bl_idname)
        self.rotate_gizmo.use_draw_modal = True
        self.rotate_gizmo.scale_basis = 0.2
        self.rotate_gizmo.color = self.transform_widget_color
        self.rotate_gizmo.alpha = self.transform_widget_alpha
        self.rotate_gizmo.color_highlight = self.transform_widget_color_highlight
        self.rotate_gizmo.alpha_highlight = self.transform_widget_alpha_highlight

        self.move_gizmo = self.gizmos.new(Physics2DShapeMoveWidget.bl_idname)
        self.move_gizmo.use_draw_modal = True
        self.move_gizmo.scale_basis = 0.4
        self.move_gizmo.color = self.transform_widget_color
        self.move_gizmo.alpha = self.transform_widget_alpha
        self.move_gizmo.color_highlight = self.transform_widget_color_highlight
        self.move_gizmo.alpha_highlight = self.transform_widget_alpha_highlight

        self.polygon_widget = self.gizmos.new(self.poly_gizmo_bl_name)
        self.polygon_widget.use_draw_scale = False


        # self.refresh_gizmos_target(context)

    def refresh(self, context: Context):
        
        self.refresh_gizmos_target(context)
        (color, alpha) = self.get_shape_widget_color_alpha(context)
        
        self.polygon_widget.color = color
        self.polygon_widget.alpha = alpha
        self.polygon_widget.color_highlight  = self.polygon_widget.color
        self.polygon_widget.alpha_highlight = self.polygon_widget.alpha

