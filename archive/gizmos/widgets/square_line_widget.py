import math
from bpy.types import (
    Gizmo,
)

from mathutils import Vector, Matrix

from ...utils.vertices import create_square_line_vertices, create_square_tris_vertices, tuple_2_to_vec_3


class SquareLineWidget(Gizmo):
    bl_idname = "VIEW3D_GT_square_line_widget"
    bl_target_properties = (
        {"id": "position", "type": 'FLOAT', "array_length": 2},
        {"id": "size", "type": 'FLOAT', "array_length": 2},        
    )
  
    __slots__ = (
        "custom_shape",
        "shape_mat",
        "orientation",
    )

    def _update_mat(self):
        if (self.target_is_valid('position')
        and hasattr(self, "orientation")      
        and self.target_is_valid('size')):

            pos2d = self.target_get_value('position')
            size2d = self.target_get_value('size')
            # orientation = self.target_get_value('orientation')
            
            position = tuple_2_to_vec_3(self.orientation,pos2d)
            size = tuple_2_to_vec_3(self.orientation,size2d)
            
            
            mat = self.matrix_basis

           

            mat = mat @ Matrix.Translation(position)
            
            mat = mat @ Matrix.Scale(size[0],4,Vector((1,0,0)))
            mat = mat @ Matrix.Scale(size[1],4,Vector((0,1,0)))
            mat = mat @ Matrix.Scale(size[2],4,Vector((0,0,1)))


            self.shape_mat = mat

    def draw(self, context):
        self._update_mat()
        if hasattr(self, "custom_shape"):
            
            self.draw_custom_shape(self.custom_shape, matrix=self.shape_mat)

    def draw_select(self, context, select_id):

        self._update_mat()
        if hasattr(self, "custom_shape"):
            self.draw_custom_shape(self.custom_shape, matrix=self.shape_mat, select_id=select_id)
        
        pass
    def setup(self):
        
        if hasattr(self, "orientation"):
            verts = (
                create_square_line_vertices(orientation = self.orientation)
            )
            
            self.custom_shape = self.new_custom_shape('LINES',verts)

            self.shape_mat = Matrix()
    
    


    # def exit(self, context, cancel):
    #     context.area.header_text_set(None)



