from math import pi
from bpy.types import Context
from mathutils import Matrix, Vector

from bpy.props import *

from ....utils import display_shape, physics_2d_enabled_on_mesh 


from ...widgets.physics_2d_polygon_widget import Physics2DPolygonWidget
from ...widgets.physics_2d_vertex_move_widget import Physics2DVertexMoveWidget
from ...widgets.physics_2d_vertex_create_widget import Physics2DVertexCreateWidget

from .physics_2d_shape_edit_gizmo import Physics2DShapeEditGizmo

class Physics2DPolygonEditGizmo(Physics2DShapeEditGizmo):
    bl_idname = "VIEW3D_GT_physics_2d_polygon_edit_gizmo"
    bl_label = "Physics 2D Polygon edit"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}
    
    poly_gizmo_bl_name = Physics2DPolygonWidget.bl_idname
    shape_type = "polygon"


    @classmethod
    def poll(cls, context):
        return physics_2d_enabled_on_mesh(context) and display_shape(context)
    

    def setup(self, context):
        self.vertex_move_widgets = list()
        self.vertex_create_widgets = list()
        super().setup(context)
        return 
    
    def refresh_shapes_widgets(self, context: Context):
        self.vertex_widget_ind = 0
        super().refresh_shapes_widgets(context)
    
    def refresh_shape_widgets(self, context: Context, shape, ind):

        super().refresh_shape_widgets(context, shape, ind)
        

        self.polygon_widgets[ind].shape_polygon_vertices =  shape.shape_polygon_vertices
        self.polygon_widgets[ind].updateShapes()
        

        vertices_pos = shape.shape_polygon_vertices
        len_vertices_move_widgets = len(self.vertex_move_widgets)
        len_vertices_pos = len(vertices_pos)
        for v_ind in range(len_vertices_pos):
            

            vertex_ind = self.vertex_widget_ind + v_ind

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

            

            vertex_pos = vertices_pos[v_ind]
            vertex_move_widget.target_set_prop('vertex_position', vertex_pos, "pos")
            vertex_move_widget.edit_ind = v_ind
            vertex_move_widget.shape = shape
            vertex_move_widget.hide = not self.display_shape_gizmos
            

            middle_vec = (Vector(vertices_pos[(v_ind + 1) % len_vertices_pos].pos) + Vector(vertex_pos.pos)) / 2.0

            vertex_create_widget.create_position = middle_vec
            vertex_create_widget.create_ind = v_ind
            vertex_create_widget.shape = shape
            vertex_create_widget.hide = not self.display_shape_gizmos

        
        self.vertex_widget_ind += len_vertices_pos
            


    def remove_shapes_widgets(self, context: Context, len_shapes, len_widgets):
        super().remove_shapes_widgets(context, len_shapes, len_widgets)

        nb_vertices = 0
        for shape in context.object.data.three_rigid_body_2d.shapes:
            if shape.shape_type == "polygon":
                nb_vertices += len(shape.shape_polygon_vertices)

        for ind_del in range(nb_vertices, len(self.vertex_move_widgets)):
            vertex_move_widget = self.vertex_move_widgets[nb_vertices]
            self.vertex_move_widgets.remove(vertex_move_widget)
            self.gizmos.remove(vertex_move_widget)

            vertex_create_widget = self.vertex_create_widgets[nb_vertices]
            self.vertex_create_widgets.remove(vertex_create_widget)
            self.gizmos.remove(vertex_create_widget)

        
        

        

    def refresh_shape_mats(self, context: Context):
        self.vertex_widget_ind = 0
        super().refresh_shape_mats(context)
       


    def refresh_shape_mat(self, context: Context, base_mat, local_mat, shape, ind_shape):
        super().refresh_shape_mat(context, base_mat, local_mat, shape, ind_shape)

        vertices_pos = shape.shape_polygon_vertices
        # len_vertices_widgets = len(self.vertex_move_widgets)
        len_vertices_pos = len(vertices_pos)

        for v_ind in range(len_vertices_pos):
            vertex_ind = self.vertex_widget_ind + v_ind
            vertex_move_widget = self.vertex_move_widgets[vertex_ind]
            vertex_create_widget = self.vertex_create_widgets[vertex_ind]

            next_vertex = vertices_pos[(v_ind + 1) % len_vertices_pos].pos

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

            widget_mat = local_mat @ Matrix.Translation(vertex_position_3)
            vertex_move_widget.matrix_basis = widget_mat

            create_vertex_mat = local_mat @ Matrix.Translation(middle_position)
            vertex_create_widget.matrix_basis = create_vertex_mat

        self.vertex_widget_ind += len_vertices_pos



    


        

        


        
        
    

  





