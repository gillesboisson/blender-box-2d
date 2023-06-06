
from mathutils import Vector, Matrix
import math
from ..physics.types import PlanDirection

from .plan import *


box_line_vertices = (
    (-1, -1, -1), (1, -1, -1),
    (1, -1, -1), (1, 1, -1),
    (1, 1, -1), (-1, 1, -1),
    (-1, 1, -1), (-1, -1, -1),

    (-1, -1, 1), (1, -1, 1),
    (1, -1, 1), (1, 1, 1),
    (1, 1, 1), (-1, 1, 1),
    (-1, 1, 1), (-1, -1, 1),
    (-1, -1, 1), (-1, -1, -1),
    (-1, 1, 1), (-1, 1, -1),
    (1, -1, 1), (1, -1, -1),
    (1, 1, 1), (1, 1, -1)
)


    
def create_box_line_vertices(
        scale: Vector=Vector((1, 1, 1)), 
        position: Vector=Vector()
    )->list[tuple[float, float, float]]:
    vertices=list()
    for box_line_vertice in box_line_vertices:
        vertices.append(
            (
                box_line_vertice[0] * scale.x + position.x,
                box_line_vertice[1] * scale.y + position.y,
                box_line_vertice[2] * scale.z + position.z
            )
        )
    return vertices


def create_cylinder_line_vertices(
        radius: float=1,
        size: float=1,
        plan_direction: PlanDirection='z',
        nb_segment: int=16,
        tube_segment_division: int=4,
        position: Vector=Vector(),
        start_angle: float=0,
        end_angle: float =2 * math.pi
    ) -> list[tuple[float, float, float]]:
    

    half_size = size / 2.0

    if plan_direction == 'X':
        cap_offset = Vector((half_size, 0, 0))
    elif plan_direction == "y":
        cap_offset = Vector((0, half_size, 0))
    else:
        cap_offset = Vector((0, 0, half_size))

    top_cap_vertices = create_circle_line_vertices(radius, plan_direction, nb_segment, Vector(
        (position.x + cap_offset.x, position.y + cap_offset.y, position.z + cap_offset.z)), start_angle, end_angle)
    bottom_cap_vertices = create_circle_line_vertices(radius, plan_direction, nb_segment, Vector(
        (position.x - cap_offset.x, position.y - cap_offset.y, position.z - cap_offset.z)), start_angle, end_angle)
    tube_vertices = list()

    for i in range(0, nb_segment, tube_segment_division):
        tube_vertices.append(top_cap_vertices[i * 2])
        tube_vertices.append(bottom_cap_vertices[i * 2])

    return top_cap_vertices + bottom_cap_vertices + tube_vertices



square_line_vertices = (
    (-0.5,-0.5), 
    (0.5,-0.5),
    (-0.5,0.5), 
    (0.5,0.5),
    (-0.5,-0.5), 
    (-0.5,0.5), 
    (0.5,-0.5),
    (0.5,0.5)

)
square_tri_vertices = (
    (-0.5,-0.5), 
    (0.5,-0.5),
    (-0.5,0.5), 
    (0.5,-0.5),
    (0.5,0.5),
    (-0.5,0.5),
)

def vertices_2d_to_vertices(vertices_2d, plan_direction='Z'):
    vertices=list()

    for  ind in range(len(vertices_2d)):
        vertices.append(tuple_2_to_vec_3(plan_direction, vertices_2d[ind]))
        
    
    return vertices


def create_square_tris_vertices(size=Vector((1,1)), plan_direction='Z',position=Vector((0,0))):
    vertices=list()
    
    for square_tri_vertex in square_tri_vertices:
        
        vertex2D = (square_tri_vertex[0] * size.x + position.x, square_tri_vertex[1] * size.y + position.y)
        vertices.append(tuple_2_to_vec_3(plan_direction, vertex2D))
        
    return vertices

def create_square_line_vertices(size=Vector((1,1)), plan_direction='Z',position=Vector((0,0))):
    vertices=list()
    
    for square_line_vertex in square_line_vertices:
        
        vertex2D = (square_line_vertex[0] * size.x + position.x, square_line_vertex[1] * size.y + position.y)
        vertices.append(tuple_2_to_vec_3(plan_direction, vertex2D))
        
    return vertices

def create_polygon_line_vertices(vertices_2d, plan_direction='Z', position=Vector((0,0))):
    vertices=list()

    for  ind in range(len(vertices_2d)):
        vertex1 = (vertices_2d[ind][0] + position.x, vertices_2d[ind][1] + position.y)
        vertex2 = (vertices_2d[(ind+1)%len(vertices_2d)][0] + position.x, vertices_2d[(ind+1)%len(vertices_2d)][1] + position.y)
        
        vertices.append(
            tuple_2_to_vec_3(plan_direction, vertex1)
        )

        vertices.append(
            tuple_2_to_vec_3(plan_direction, vertex2)
        )
    
    return vertices

def create_circle_line_vertices(
        radius: float = 1,
        plan_direction: PlanDirection = 'Z',
        nb_segment: int = 32,
        position: Vector = Vector(),
        start_angle: float = 0,
        end_angle: float = 2 * math.pi
    ):
    vertices=list()

    angle_segment = (end_angle - start_angle) / nb_segment

    for i in range(nb_segment+1):
        angle = i * angle_segment + start_angle
        
        vertex2D = (math.cos(angle) * radius + position.x, math.sin(angle) * radius + position.y)

        if i != 0:
            vertices.append(tuple_2_to_vec_3(plan_direction, lastVertex2D))
            vertices.append(tuple_2_to_vec_3(plan_direction, vertex2D))

        

        lastVertex2D = vertex2D
    return vertices



def create_circle_tris_vertices(
        radius: float = 1,
        plan_direction: PlanDirection = 'Z',
        nb_segment: int = 32,
        position: Vector = Vector(),
        start_angle: float = 0,
        end_angle: float = 2 * math.pi
    ):
    vertices=list()

    angle_segment = (end_angle - start_angle) / nb_segment

    for i in range(nb_segment+1):
        angle = i * angle_segment + start_angle
        
        vertex2D = (math.cos(angle) * radius + position.x, math.sin(angle) * radius + position.y)

        if i != 0:
            vertices.append(tuple_2_to_vec_3(plan_direction, lastVertex2D))
            vertices.append(tuple_2_to_vec_3(plan_direction, vertex2D))
            vertices.append(tuple_2_to_vec_3(plan_direction, position.to_tuple()))

        

        lastVertex2D = vertex2D
    return vertices