import math
from bpy.types import (
    Gizmo,
)

from mathutils import Vector, Matrix

from ..utils.vertices import create_box_line_vertices,create_circle_vertices, create_cylinder_vertices


class SphereWidget(Gizmo):
    bl_idname = "VIEW3D_GT_sphere_widget"
    bl_target_properties = (
        {"id": "radius", "type": 'FLOAT', "array_length": 1},
        {"id": "translation", "type": 'FLOAT', "array_length": 3},
    )

    __slots__ = (
        "custom_shape",
        "shape_mat",
    )

    def _update_mat(self):
        if (self.target_is_valid('radius') 
        and self.target_is_valid('translation')):
            mat = self.matrix_basis
            
            mat = mat @ Matrix.Translation(Vector(self.target_get_value('translation')))
            
            mat = mat @ Matrix.Scale(self.target_get_value('radius'),4,Vector((1,0,0)))
            mat = mat @ Matrix.Scale(self.target_get_value('radius'),4,Vector((0,1,0))) 
            mat = mat @ Matrix.Scale(self.target_get_value('radius'),4,Vector((0,0,1)))

            self.shape_mat = mat

    def draw(self, context):
        self._update_mat()
        self.draw_custom_shape(self.custom_shape, matrix=self.shape_mat)

    def draw_select(self, context, select_id):
        self._update_mat()
        self.draw_custom_shape(self.custom_shape, matrix=self.shape_mat, select_id=select_id)
        pass

    def setup(self):
        if not hasattr(self, "custom_shape"):
            verts = (
                create_circle_vertices(1, orientation="z") +
                create_circle_vertices(1,orientation="x") +
                create_circle_vertices(1,orientation="y")
            )

            self.custom_shape = self.new_custom_shape('LINES',verts)
        self.shape_mat = Matrix()
    
    
    def invoke(self, context, event):
        self.init_mouse_y = event.mouse_y

        

        return {'RUNNING_MODAL'}

    def exit(self, context, cancel):
        context.area.header_text_set(None)