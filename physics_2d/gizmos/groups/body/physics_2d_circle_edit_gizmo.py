from math import pi
from mathutils import Matrix, Vector
from ...widgets.physics_2d_shape_radius_widget import Physics2DShapeRadiusWidget
from ...widgets.physics_2d_shape_scale_widget import Physics2DShapeScaleWidget
from ...widgets.physics_2d_shape_move_widget import Physics2DShapeMoveWidget
from ...widgets.physics_2d_shape_rotate_widget import Physics2DShapeRotateWidget
from .....utils.plan import  clamp_matrix_to_plan, get_plan_matrix

from bpy.types import (Context, GizmoGroup, Operator)
from bpy.props import *

from ..physics_2d_shape_edit_gizmo import Physics2DEditGizmo



from ....utils import display_shape, physics_2d_can_edit_circle_shape, physics_2d_can_edit_square_shape 

from ...widgets.physics_2d_circle_widget import Physics2DCircleWidget

class Physics2DCircleEditGizmo(Physics2DEditGizmo):
    bl_idname = "VIEW3D_GT_physics_2d_circle_edit_gizmo"
    bl_label = "Physics 2D Circle Edit Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    poly_gizmo_bl_name = Physics2DCircleWidget.bl_idname

    @classmethod
    def poll(cls, context):
        return physics_2d_can_edit_circle_shape(context) and display_shape(context)




    def setup(self, context):



        
        super().setup(context)

        self.rotate_gizmo.hide = True

        self.radius_gizmo = self.gizmos.new(Physics2DShapeRadiusWidget.bl_idname)
        self.radius_gizmo.use_draw_modal = True
        self.radius_gizmo.scale_basis = 0.2
        self.radius_gizmo.color = self.transform_widget_color
        self.radius_gizmo.alpha = self.transform_widget_alpha
        self.radius_gizmo.color_highlight = self.transform_widget_color_highlight
        self.radius_gizmo.alpha_highlight = self.transform_widget_alpha_highlight

        return 
    
    def refresh_gizmos_target(self, context):
    


        super().refresh_gizmos_target(context)
        self.radius_gizmo.target_set_prop('shape_radius', context.object.data.three_rigid_body_2d.shape,"shape_radius")


    def draw_prepare(self, context):
        shape = context.object.data.three_rigid_body_2d.shape

        base_mat = self.get_widget_base_matrix(context)

        scale_mat = Matrix.Scale(shape.shape_radius,4,(0,0,1))
        scale_mat = scale_mat @ Matrix.Scale(shape.shape_radius,4,(0,1,0))
        scale_mat = scale_mat @ Matrix.Scale(shape.shape_radius,4,(1,0,0))

        scale_offset_mat = Matrix.Translation(Vector((shape.shape_radius,0,0.0)))
        self.move_gizmo.matrix_basis = base_mat 
        self.radius_gizmo.matrix_basis =  base_mat @ scale_offset_mat
        self.polygon_widget.matrix_basis =  base_mat @ scale_mat 



        

        


        
        
    

  





