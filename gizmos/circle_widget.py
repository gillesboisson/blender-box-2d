import math
from bpy.types import (
    Gizmo,
)

from mathutils import Vector, Matrix

from ..utils.vertices import create_circle_vertices, get_x_transposition_vector, get_y_transposition_vector, vec_2_to_vec_3


class CircleWidget(Gizmo):
    bl_idname = "VIEW3D_GT_circle_widget"
    bl_target_properties = (
        {"id": "position", "type": 'FLOAT', "array_length": 2},
        {"id": "radius", "type": 'FLOAT'},        
    )

    __slots__ = (
        "custom_shape",
        "shape_mat",
        "orientation",

    )

    def _update_mat(self):
        if (self.target_is_valid('position')
        and hasattr(self, "orientation") 
        and self.target_is_valid('radius')):

            pos2d = self.target_get_value('position')
            
            position = vec_2_to_vec_3(self.orientation,pos2d)

            radius = self.target_get_value('radius')

            
            mat = self.matrix_basis

           

            mat = mat @ Matrix.Translation(position)
            
            mat = mat @ Matrix.Scale(radius,4,Vector((1,0,0)))
            mat = mat @ Matrix.Scale(radius,4,Vector((0,1,0)))
            mat = mat @ Matrix.Scale(radius,4,Vector((0,0,1)))

            self.shape_mat = mat

    def draw(self, context):
        self._update_mat()
        # self.draw_preset_circle(self.shape_mat,axis="POS_Z")
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
                create_circle_vertices(orientation = self.orientation)
            )
            

            self.custom_shape = self.new_custom_shape('LINES',verts)
            self.shape_mat = Matrix()
    
    
    def invoke(self, context, event):
        self.init_mouse_y = event.mouse_y
        return {'RUNNING_MODAL'}

    def exit(self, context, cancel):
        context.area.header_text_set(None)