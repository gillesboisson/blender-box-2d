from .physics_2d_widget import Physics2DWidget
from ...types import PlanDirection
from ....utils.vertices import create_polygon_line_vertices


class Physics2DPolygonWidget(Physics2DWidget):

    bl_idname = "VIEW3D_GT_three_physics_2d_polygon_widget"

    # bl_target_properties = (
    #     {"id": "shape_polygon_vertices", "type": 'COLLECTION'},
    # )

    vertices = list()

    

    def draw(self, context):
        self.updateShapes()
        return super().draw(context)
    
    def draw_select(self, context, select_id):
        self.updateShapes()
        return super().draw_select(context, select_id)
    
    def updateShapes(self):
        self.shapes = list()
        

        if(hasattr(self, 'shape_polygon_vertices')):
            vertices = list()
            for vertex in self.shape_polygon_vertices:
                vertices.append((vertex.pos[0], vertex.pos[1]))
            if(len(vertices) > 0):
                tri_vertices = create_polygon_line_vertices(vertices)
                self.shapes.append(self.new_custom_shape('LINES',tri_vertices))

           