

from math import pi
from bpy.types import Context
from mathutils import Matrix, Vector
from ...widgets.physics_2d_square_widget import Physics2DSquareWidget


from bpy.props import *


from ....utils import display_shape_gizmos, physics_2d_enabled_on_mesh 

from ...widgets.physics_2d_shape_scale_widget import Physics2DShapeScaleWidget
from .physics_2d_shape_edit_gizmo import Physics2DShapeEditGizmo


class Physics2DSquareEditGizmo(Physics2DShapeEditGizmo):
    bl_idname = "VIEW3D_GT_physics_2d_square_edit_gizmo"
    bl_label = "Physics 2D Square Edit Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}


    @classmethod
    def poll(cls, context):
        return physics_2d_enabled_on_mesh(context) and display_shape_gizmos(context)

    poly_gizmo_bl_name = Physics2DSquareWidget.bl_idname
    shape_type = "box"
    def refresh_shape_widgets(self, context: Context, shape, ind):

        super().refresh_shape_widgets(context, shape, ind)

        if(len(self.scale_widgets) <= ind):
            scale_widget = self.gizmos.new(Physics2DShapeScaleWidget.bl_idname)
            self.scale_widgets.append(scale_widget)
            scale_widget.use_draw_modal = True
            scale_widget.scale_basis = 0.2
            scale_widget.color = self.transform_widget_color
            scale_widget.alpha = self.transform_widget_alpha
            scale_widget.color_highlight = self.transform_widget_color_highlight
            scale_widget.alpha_highlight = self.transform_widget_alpha_highlight
        else:
            scale_widget = self.scale_widgets[ind]

        scale_widget.hide = not self.display_shape_gizmos
        

        scale_widget.target_set_prop('shape_scale', shape,"shape_box_scale")
        scale_widget.target_set_prop('shape_position', shape,"shape_position")
    

    def remove_shape_widget(self, ind_shape):

        super().remove_shape_widget(ind_shape)
        self.gizmos.remove(self.scale_widgets[ind_shape])
        del self.scale_widgets[ind_shape]


    def scale_mat(self, context: Context, shape, ind_shape):
        return Matrix.Scale(shape.shape_box_scale[0],4,(1,0,0)) @ Matrix.Scale(shape.shape_box_scale[1],4,(0,1,0))
    
    def refresh_shape_mat(self, context: Context, base_mat, local_mat, shape, ind_shape):
        super().refresh_shape_mat(context, base_mat, local_mat, shape, ind_shape)

        scale_widget = self.scale_widgets[ind_shape]
        scale_offset_mat = Matrix.Translation(Vector((shape.shape_box_scale[0] / 2,shape.shape_box_scale[1] / 2,0.0))) @ self.cached_object_inv_scale_mat

        scale_widget.matrix_basis = local_mat @ scale_offset_mat

    def setup(self, context):
        self.scale_widgets = list()
        super().setup(context)


        

        


        
        
    

  





