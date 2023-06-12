

from math import pi
from bpy.types import Context
from mathutils import Matrix, Vector
from ...widgets.physics_2d_square_widget import Physics2DSquareWidget

from ..physics_2d_shape_edit_gizmo import Physics2DEditGizmo

from bpy.props import *


from ....utils import display_shape, physics_2d_can_edit_square_shape 

from ...widgets.physics_2d_shape_scale_widget import Physics2DShapeScaleWidget


class Physics2DSquareEditGizmo(Physics2DEditGizmo):
    bl_idname = "VIEW3D_GT_physics_2d_square_edit_gizmo"
    bl_label = "Physics 2D Square Edit Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}


    @classmethod
    def poll(cls, context):
        return physics_2d_can_edit_square_shape(context) and display_shape(context)

    poly_gizmo_bl_name = Physics2DSquareWidget.bl_idname
    
        
    def setup(self, context):

        super().setup(context)

        self.scale_gizmo = self.gizmos.new(Physics2DShapeScaleWidget.bl_idname)
        self.scale_gizmo.use_draw_modal = True
        self.scale_gizmo.scale_basis = 0.2
        self.scale_gizmo.color = self.transform_widget_color
        self.scale_gizmo.alpha = self.transform_widget_alpha
        self.scale_gizmo.color_highlight = self.transform_widget_color_highlight
        self.scale_gizmo.alpha_highlight = self.transform_widget_alpha_highlight




        return 
    
    def refresh_gizmos_target(self, context):

        super().refresh_gizmos_target(context)
        self.scale_gizmo.target_set_prop('shape_scale', context.object.data.three_rigid_body_2d.shape,"shape_box_scale")

        display_shape_gizmos = context.scene.three_physics.physics_2d_viewport_settings.display_shape_gizmos
        self.scale_gizmo.hide = not display_shape_gizmos

    def refresh(self, context: Context):
        return super().refresh(context)
    

    
    def draw_prepare(self, context):
        shape = context.object.data.three_rigid_body_2d.shape

        scale_mat = Matrix.Scale(shape.shape_box_scale[0],4,(1,0,0)) @ Matrix.Scale(shape.shape_box_scale[1],4,(0,1,0)) 
        
        base_mat = self.get_widget_base_matrix(context)
        base_mat @= Matrix.Rotation(shape.shape_angle * pi / 180.0, 4, 'Z')

        scale_offset_mat = Matrix.Translation(Vector((shape.shape_box_scale[0] / 2,shape.shape_box_scale[1] / 2,0.0)))

        self.move_gizmo.matrix_basis = base_mat 
        self.rotate_gizmo.matrix_basis =  base_mat #@ rotation_offset_mat
        self.scale_gizmo.matrix_basis =  base_mat @ scale_offset_mat

        self.polygon_widget.matrix_basis =  base_mat @ scale_mat



        

        


        
        
    

  





