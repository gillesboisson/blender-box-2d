from math import pi
from bpy.types import Context
from mathutils import Matrix, Vector

from bpy.props import *

from ...utils import physics_2d_can_edit_polygon_shape 
from .physics_2d_shape_edit_gizmo import Physics2DEditGizmo


from ..widgets.physics_2d_polygon_widget import Physics2DPolygonWidget
from ..widgets.physics_2d_vertex_move_widget import Physics2DVertexMoveWidget
from ..widgets.physics_2d_vertex_create_widget import Physics2DVertexCreateWidget


class Physics2DPolygonEditGizmo(Physics2DEditGizmo):
    bl_idname = "VIEW3D_GT_physics_2d_polygon_edit_gizmo"
    bl_label = "Physics 2D Polygon edit"
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
        self.polygon_widget.shape_polygon_vertices = context.object.data.three_rigid_body_2d.shape.shape_polygon_vertices

        super().setup(context)

        self.vertex_move_widgets = list()
        self.vertex_create_widgets = list()

        self.update_vertex_widgets(context)
      
        return 
    
    
    def update_vertex_widgets(self, context: Context, set_prop = True):
        vertices_pos = context.object.data.three_rigid_body_2d.shape.shape_polygon_vertices

        len_vertices_move_widgets = len(self.vertex_move_widgets)
        len_vertices_pos = len(vertices_pos)

        v_len = max(len_vertices_move_widgets, len_vertices_pos)

        for vertex_ind in range(len_vertices_pos):

            if vertex_ind >= len_vertices_move_widgets:
                vertex_create_widget =  self.gizmos.new(Physics2DVertexCreateWidget.bl_idname)
                vertex_create_widget.use_draw_modal = False
                vertex_create_widget.color = 0.8, 0.8, 0.8
                vertex_create_widget.alpha = self.transform_widget_alpha * 0.2
                vertex_create_widget.color_highlight  =  1,1,1
                vertex_create_widget.alpha_highlight = self.transform_widget_alpha_highlight
                vertex_create_widget.scale_basis = 0.1
                
                self.vertex_create_widgets.append(vertex_create_widget)
            else:
                vertex_create_widget = self.vertex_create_widgets[vertex_ind]

            if vertex_ind >= len_vertices_move_widgets :
                vertex_move_widget =  self.gizmos.new(Physics2DVertexMoveWidget.bl_idname)
                vertex_move_widget.use_draw_modal = True
                vertex_move_widget.color = 0.8, 0.8, 0.8
                vertex_move_widget.alpha = self.transform_widget_alpha
                vertex_move_widget.color_highlight  =  1,1,1
                vertex_move_widget.alpha_highlight = self.transform_widget_alpha_highlight
                vertex_move_widget.scale_basis = 0.1
                self.vertex_move_widgets.append(vertex_move_widget)

            else:
                vertex_move_widget = self.vertex_move_widgets[vertex_ind]

            if vertex_ind < len_vertices_pos:
                vertex_pos = vertices_pos[vertex_ind]
                if set_prop:
                    vertex_move_widget.target_set_prop('vertex_position', vertex_pos, "pos")

                vertex_move_widget.edit_ind = vertex_ind


                middle_vec = (Vector(vertices_pos[(vertex_ind + 1) % len_vertices_pos].pos) + Vector(vertex_pos.pos)) / 2.0

                vertex_create_widget.create_position = middle_vec
                vertex_create_widget.create_ind = vertex_ind

            else:
                vertex_move_widget.hide = True
                vertex_create_widget.hide = True

        if len_vertices_move_widgets > len_vertices_pos:
            for vertex_ind in range(len_vertices_pos, len_vertices_move_widgets):
                vertex_move_widget = self.vertex_move_widgets[vertex_ind]
                self.vertex_move_widgets.remove(vertex_move_widget)
                self.gizmos.remove(vertex_move_widget)

                vertex_create_widget = self.vertex_create_widgets[vertex_ind]
                self.vertex_create_widgets.remove(vertex_create_widget)
                self.gizmos.remove(vertex_create_widget)
        


    def refresh(self, context: Context):
        self.update_vertex_widgets(context, True)
        self.refresh_gizmos_target(context)
        self.polygon_widget.shape_polygon_vertices = context.object.data.three_rigid_body_2d.shape.shape_polygon_vertices

     
    def draw_prepare(self, context):
        # print("draw_prepare")
        shape = context.object.data.three_rigid_body_2d.shape

        base_mat = self.get_widget_base_matrix(context)
        base_mat @= Matrix.Rotation(shape.shape_angle * pi / 180.0, 4, 'Z')

        self.move_gizmo.matrix_basis = base_mat
        self.rotate_gizmo.matrix_basis = base_mat #@ rotation_offset_mat 
        
        self.polygon_widget.matrix_basis =  base_mat 
        
        vertices_pos = context.object.data.three_rigid_body_2d.shape.shape_polygon_vertices
        len_vertices_widgets = len(self.vertex_move_widgets)
        len_vertices_pos = len(vertices_pos)

        v_len = min(len_vertices_widgets, len_vertices_pos)

        for ind in range(v_len):
            vertex_move_widget = self.vertex_move_widgets[ind]
            vertex_create_widget = self.vertex_create_widgets[ind]

            next_vertex = vertices_pos[(ind + 1) % len_vertices_pos].pos

            next_vertex_position_3 = Vector((
                next_vertex[0],
                next_vertex[1],
                0.0)
            )

            vertex_position_3 = Vector((
                vertex_move_widget.target_get_value("vertex_position")[0],
                vertex_move_widget.target_get_value("vertex_position")[1],
                0.0)
            )

            middle_position = (next_vertex_position_3 + vertex_position_3) / 2.0

            widget_mat = base_mat @ Matrix.Translation(vertex_position_3)
            vertex_move_widget.matrix_basis = widget_mat

            create_vertex_mat = base_mat @ Matrix.Translation(middle_position)
            vertex_create_widget.matrix_basis = create_vertex_mat


    


        

        


        
        
    

  





