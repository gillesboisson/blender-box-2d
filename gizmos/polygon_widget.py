import math
from bpy.types import (
    Gizmo,
)

from mathutils import Vector, Matrix

from ..utils.vertices import create_polygon_vertices, vec_2_to_vec_3

class PolygonWidget(Gizmo):
    bl_idname = "VIEW3D_GT_polygon_widget"
    bl_target_properties = (
        {"id": "position", "type": 'FLOAT', "array_length": 2},

    )

    __slots__ = (
        "orientation",
        "shape_mat",
        "custom_shape",
        "vertices",
    )

    def _update_mat(self):
        if (self.target_is_valid('position')):
            mat = self.matrix_basis
            pos2d = self.target_get_value('position')
            
            position = vec_2_to_vec_3(self.orientation,pos2d)
            
            mat = mat @ Matrix.Translation(Vector(position))

            self.shape_mat = mat

    def draw(self, context):
        self.setup()

        self._update_mat()
        # if(hasattr(self,"custom_shape")):
        #     self.draw_custom_shape(self.custom_shape, matrix=self.shape_mat)

    def draw_select(self, context, select_id):
        self.setup()

        self._update_mat()
        # if(hasattr(self,"custom_shape")):
        #     self.draw_custom_shape(self.custom_shape, matrix=self.shape_mat, select_id=select_id)
        pass

    def setup(self):
        if hasattr(self, "vertices"):
            verts2D = list()
            for v in self.vertices:
                verts2D.append((v.pos[0],v.pos[1]))
            # self.vertices.map(lambda v: v.pos) 

            verts = create_polygon_vertices(verts2D, self.orientation)
            
            if(len(verts) > 0):
                self.custom_shape = self.new_custom_shape('LINES',verts)

        
        self.shape_mat = Matrix()
    
    
    def invoke(self, context, event):
        self.init_mouse_y = event.mouse_y


        return {'RUNNING_MODAL'}

    def exit(self, context, cancel):
        context.area.header_text_set(None)