
from ...utils.draw import draw_polyline, draw_polyline_2D

def selectedObjectHasPhysics2DPolygonShape(context):
    return context.active_object is not None and context.active_object.data.three_rigid_body_2d and context.active_object.data.three_rigid_body_2d.enabled and context.active_object.data.three_rigid_body_2d.shape.shape_type == 'polygon'


def removeVertexToShape(context, index):
    context.active_object.data.three_rigid_body_2d.shape.shape_polygon_vertices.remove(index)

def addVertexToShape(context):
    context.active_object.data.three_rigid_body_2d.shape.shape_polygon_vertices.add()

def draw_vertices(self, context):
    polygon_vertices = context.active_object.data.three_rigid_body_2d.shape.shape_polygon_vertices
    vertices2D = list()

    for ind in range(len(polygon_vertices)):
        if(ind == self.vertex_index):
            vertices2D.append((self.editedVertex.pos[0],self.editedVertex.pos[1]))
        else:
            vertices2D.append((polygon_vertices[ind].pos[0],polygon_vertices[ind].pos[1]))

    draw_polyline_2D(vertices2D, (1,1,0,1), context.scene.three_physics.physics_2d_orientation, self.mat)


def draw_poly_vertices(self, context):
    # mat = context.active_object.matrix_world.copy()
    polygon_vertices = context.active_object.data.three_rigid_body_2d.shape.shape_polygon_vertices
    display_shape = context.scene.three_physics.physics_2d_display_shape
    
    if(not display_shape): return 
    
    vertices2D = list()
    for vertex in polygon_vertices:
        vertices2D.append((vertex.pos[0],vertex.pos[1]))

    draw_polyline_2D(vertices2D, (1,1,0,1), context.scene.three_physics.physics_2d_orientation, context.active_object.matrix_world)
