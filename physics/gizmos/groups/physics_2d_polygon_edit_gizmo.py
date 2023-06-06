from math import pi
from mathutils import Matrix

from bpy.props import *

from ...utils import physics_2d_can_edit_polygon_shape 
from .physics_2d_shape_edit_gizmo import Physics2DEditGizmo


from ..widgets.physics_2d_polygon_widget import Physics2DPolygonWidget

class Physics2DPolygonEditGizmo(Physics2DEditGizmo):
    bl_idname = "VIEW3D_GT_physics_2d_polygon_edit_gizmo"
    bl_label = "Physics 2D Circle Edit Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}


    @classmethod
    def poll(cls, context):
        return physics_2d_can_edit_polygon_shape(context)


    def setup(self, context):
        (color, alpha) = self.get_shape_widget_color_alpha(context)

        self.polygon_widget = self.gizmos.new(Physics2DPolygonWidget.bl_idname)
        self.polygon_widget.use_draw_scale = False
        self.polygon_widget.color = color
        self.polygon_widget.alpha = alpha
        self.polygon_widget.color_highlight  = self.polygon_widget.color
        self.polygon_widget.alpha_highlight = self.polygon_widget.alpha

        super().setup(context)
        self.polygon_widget.shape_polygon_vertices = context.object.data.three_rigid_body_2d.shape.shape_polygon_vertices

        return 
    


    def draw_prepare(self, context):
        shape = context.object.data.three_rigid_body_2d.shape

        base_mat = self.get_widget_base_matrix(context)
        base_mat @= Matrix.Rotation(shape.shape_angle * pi / 180.0, 4, 'Z')

        self.move_gizmo.matrix_basis = base_mat
        self.rotate_gizmo.matrix_basis = base_mat #@ rotation_offset_mat 
        
        self.polygon_widget.matrix_basis =  base_mat 



        

        


        
        
    

  





