

from math import pi
from mathutils import Matrix, Vector
from ....utils.plan import  clamp_matrix_to_plan, get_plan_matrix

from bpy.types import (Context, GizmoGroup, Operator)
from bpy.props import *
import bpy


from ...utils import physics_2d_can_edit_circle_shape, physics_2d_can_edit_square_shape 

from ..widgets.physics_2d_shape_widgets import PhysicsCircleWidget, ShapeMoveWidget, ShapeRadiusWidget, ShapeRotateWidget, ShapeScaleWidget





class Physics2DCircleEditGizmo(GizmoGroup):
    bl_idname = "VIEW3D_GT_physics_2d_circle_edit_gizmo"
    bl_label = "Physics 2D Circle Edit Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}


    @classmethod
    def poll(cls, context):
        return physics_2d_can_edit_circle_shape(context)


    def setup(self, context):

        self.circle_widget = self.gizmos.new(PhysicsCircleWidget.bl_idname)
        self.circle_widget.use_draw_scale = False
        

        if(context.object.data.three_rigid_body_2d.body_type == 'static'):
            self.circle_widget.color = 0.5, 1.0, 0.5
            self.circle_widget.alpha = 0.8
            self.circle_widget.color_highlight  = self.circle_widget.color
            self.circle_widget.alpha_highlight = self.circle_widget.alpha
        elif(context.object.data.three_rigid_body_2d.body_type == 'dynamic'):
            self.circle_widget.color = 0.5, 0.5, 1.0
            self.circle_widget.alpha = 0.8
            self.circle_widget.color_highlight  = self.circle_widget.color
            self.circle_widget.alpha_highlight = self.circle_widget.alpha
        else:
            self.circle_widget.color = 0.5, 0.5, 0.5
            self.circle_widget.alpha = 0.8
            self.circle_widget.color_highlight  = self.circle_widget.color
            self.circle_widget.alpha_highlight = self.circle_widget.alpha


        gz = self.gizmos.new(ShapeMoveWidget.bl_idname)
        gz.target_set_prop('shape_position', context.object.data.three_rigid_body_2d.shape,"shape_position")
        gz.use_draw_modal = True

        # gz.matrix_basis =  context.object.matrix_world
        gz.scale_basis = 0.4
        self.move_gizmo = gz

        # gz.target_set_handler("offset", get=get_shape_position, set=set_shape_position, range=shape_range)
        
        # gz.use_draw_value = True

        gz.color = 0.8, 0.8, 1.0
        gz.alpha = 0.5

        gz.color_highlight = 0.5, 0.5, 1.0
        gz.alpha_highlight = 1.0

        # self.rotate_gizmo = self.gizmos.new(ShapeRotateWidget.bl_idname)
        # self.rotate_gizmo.target_set_prop('shape_angle', context.object.data.three_rigid_body_2d.shape,"shape_angle")
        # self.rotate_gizmo.target_set_prop('shape_position', context.object.data.three_rigid_body_2d.shape,"shape_position")
        # self.rotate_gizmo.use_draw_modal = True
        # self.rotate_gizmo.scale_basis = 0.2
        # self.rotate_gizmo.color = 0.8, 0.8, 1.0
        # self.rotate_gizmo.alpha = 0.5
        # self.rotate_gizmo.color_highlight = 0.5, 0.5, 1.0
        # self.rotate_gizmo.alpha_highlight = 1.0

        self.radius_gizmo = self.gizmos.new(ShapeRadiusWidget.bl_idname)
        self.radius_gizmo.target_set_prop('shape_radius', context.object.data.three_rigid_body_2d.shape,"shape_radius")
        self.radius_gizmo.use_draw_modal = True
        self.radius_gizmo.scale_basis = 0.2
        self.radius_gizmo.color = 0.8, 0.8, 1.0
        self.radius_gizmo.alpha = 0.5
        self.radius_gizmo.color_highlight = 0.5, 0.5, 1.0
        self.radius_gizmo.alpha_highlight = 1.0

        # # gz.is_modal = True
        # gz.scale_basis = 0.2

        # self.gizmo_move = gz
        
        return 
    


    def draw_prepare(self, context):
        shape = context.object.data.three_rigid_body_2d.shape

        matrix_world = context.object.matrix_world
        plan_direction = context.scene.three_physics.physics_2d_orientation

        # create box scale matrix
        orientation_mat = get_plan_matrix(plan_direction)
        clamp_world_mat = clamp_matrix_to_plan(plan_direction, matrix_world)
        
        
        local_mat = Matrix.Translation(Vector((shape.shape_position[0],shape.shape_position[1],0.0)))
        # local_mat @= Matrix.Rotation(shape.shape_angle * pi / 180.0, 4, 'Z')
        # scale_mat = Matrix.Scale(shape.shape_box_scale[0],4,(1,0,0)) @ Matrix.Scale(shape.shape_box_scale[1],4,(0,1,0)) 
        
        base_mat = clamp_world_mat @ orientation_mat @ local_mat

        scale_mat = Matrix.Scale(shape.shape_radius,4,(0,0,1))
        scale_mat = scale_mat @ Matrix.Scale(shape.shape_radius,4,(0,1,0))
        scale_mat = scale_mat @ Matrix.Scale(shape.shape_radius,4,(1,0,0))

        scale_offset_mat = Matrix.Translation(Vector((shape.shape_radius,0,0.0)))
        # rotation_offset_mat = Matrix.Translation(Vector((shape.shape_box_scale[0] / 2,0,0)))

        # if(hasattr(self, 'move_gizmo') ): 
        self.move_gizmo.matrix_basis = base_mat 
        # self.rotate_gizmo.matrix_basis =  base_mat @ rotation_offset_mat
        self.radius_gizmo.matrix_basis =  base_mat @ scale_offset_mat

        # if(hasattr(self, 'circle_widget')):
        self.circle_widget.matrix_basis =  base_mat @ scale_mat 



        

        


        
        
    

  





