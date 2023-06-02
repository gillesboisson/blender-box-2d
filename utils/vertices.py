
from mathutils import Vector, Matrix
import math


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

def create_box_line_vertices(scale=Vector((1, 1, 1)), position=Vector()):
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


def create_cylinder_vertices(radius=1, size=1, orientation='z', nb_segment=16, tube_segment_division=4, position=Vector(), start_angle=0, end_angle=2 * math.pi):
    

    half_size = size / 2.0

    if orientation == "x":
        cap_offset = Vector((half_size, 0, 0))
    elif orientation == "y":
        cap_offset = Vector((0, half_size, 0))
    else:
        cap_offset = Vector((0, 0, half_size))

    top_cap_vertices = create_circle_vertices(radius, orientation, nb_segment, Vector(
        (position.x + cap_offset.x, position.y + cap_offset.y, position.z + cap_offset.z)), start_angle, end_angle)
    bottom_cap_vertices = create_circle_vertices(radius, orientation, nb_segment, Vector(
        (position.x - cap_offset.x, position.y - cap_offset.y, position.z - cap_offset.z)), start_angle, end_angle)
    tube_vertices = list()

    for i in range(0, nb_segment, tube_segment_division):
        tube_vertices.append(top_cap_vertices[i * 2])
        tube_vertices.append(bottom_cap_vertices[i * 2])

    return top_cap_vertices + bottom_cap_vertices + tube_vertices


def get_x_transposition_vector(orientation =""):
    if orientation == "x":
        return Vector((0, 1, 0))
    elif orientation == "y":
        return Vector((0, 0, 1))
    else:
        return Vector((1, 0, 0))
    
def get_y_transposition_vector(orientation =""):
    if orientation == "x":
        return Vector((0, 0, 1))
    elif orientation == "y":
        return Vector((1, 0, 0))
    else:
        return Vector((0, 1, 0))

def vec_2_to_vec_3(orientation, vec_2):
    if orientation == "x":
        return Vector((0, vec_2[0], vec_2[1]))
    elif orientation == "y":
        return Vector((vec_2[0], 0, vec_2[1]))
    else:
        return Vector((vec_2[0], vec_2[1], 0))

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

def vertices2DToVertices(vertices_2d, orientation='z'):
    vertices=list()

    if orientation == "x":
        mat_coef_x = (0, 1, 0)
        mat_coef_y = (0, 0, 1)
    elif orientation == "y":
        mat_coef_x = (0, 0, 1)
        mat_coef_y = (1, 0, 0)
    else:
        mat_coef_x = (1, 0, 0)
        mat_coef_y = (0, 1, 0)

    for  ind in range(len(vertices_2d)):
        x = vertices_2d[ind][0]
        y = vertices_2d[ind][1]
        # print(ind)
        vertices.append(
            (
                x * mat_coef_x[0] + y * mat_coef_y[0] ,
                x * mat_coef_x[1] + y * mat_coef_y[1] ,
                x * mat_coef_x[2] + y * mat_coef_y[2]
            )
        )
    
    return vertices


def create_square_vertices(size=Vector((1,1,1)), orientation='z',position=Vector((0,0,0))):
    vertices=list()

    # calculate matrix coef based on orientation
    if orientation == "x":
        mat_coef_x = (0, 1, 0)
        mat_coef_y = (0, 0, 1)
    elif orientation == "y":
        mat_coef_x = (0, 0, 1)
        mat_coef_y = (1, 0, 0)
    else:
        mat_coef_x = (1, 0, 0)
        mat_coef_y = (0, 1, 0)

    
    for square_line_vertice in square_line_vertices:
        x = square_line_vertice[0] * size.x + position.x
        y = square_line_vertice[1] * size.y + position.y

        # apply matrix coef
        vertices.append(
            (
                x * mat_coef_x[0] + y * mat_coef_y[0] ,
                x * mat_coef_x[1] + y * mat_coef_y[1] ,
                x * mat_coef_x[2] + y * mat_coef_y[2]
            )
        )

    return vertices

def create_polygon_vertices(vertices_2d, orientation='z', position=Vector((0,0,0))):
    vertices=list()

    if orientation == "x":
        mat_coef_x = (0, 1, 0)
        mat_coef_y = (0, 0, 1)
    elif orientation == "y":
        mat_coef_x = (0, 0, 1)
        mat_coef_y = (1, 0, 0)
    else:
        mat_coef_x = (1, 0, 0)
        mat_coef_y = (0, 1, 0)

    for  ind in range(len(vertices_2d)):
        x1 = vertices_2d[ind][0] + position.y
        y1 = vertices_2d[ind][1] + position.z
        x2 = vertices_2d[(ind+1)%len(vertices_2d)][0] + position.y
        y2 = vertices_2d[(ind+1)%len(vertices_2d)][1] + position.z
        # print(ind)
        vertices.append(
            (
                x1 * mat_coef_x[0] + y1 * mat_coef_y[0] ,
                x1 * mat_coef_x[1] + y1 * mat_coef_y[1] ,
                x1 * mat_coef_x[2] + y1 * mat_coef_y[2]
            )
        )

        # add second vertice
        vertices.append(
            (        
                x2 * mat_coef_x[0] + y2 * mat_coef_y[0] ,
                x2 * mat_coef_x[1] + y2 * mat_coef_y[1] ,
                x2 * mat_coef_x[2] + y2 * mat_coef_y[2]
            )
        )
    
    return vertices


                


def create_circle_vertices(radius=1, orientation='z', nb_segment=32, position=Vector(), start_angle=0, end_angle=2 * math.pi):
    vertices=list()

    last_x = 0
    last_y = 0
    angle_segment = (end_angle - start_angle) / nb_segment

    if orientation == "x":
        mat_coef_x = (0, 1, 0)
        mat_coef_y = (0, 0, 1)
    elif orientation == "y":
        mat_coef_x = (0, 0, 1)
        mat_coef_y = (1, 0, 0)
    else:
        mat_coef_x = (1, 0, 0)
        mat_coef_y = (0, 1, 0)

    for i in range(nb_segment+1):
        angle = i * angle_segment + start_angle
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius

        if i != 0:
            vertices.append(
                (
                    last_x * mat_coef_x[0] + last_y *
                    mat_coef_y[0] + position.x,
                    last_x * mat_coef_x[1] + last_y *
                    mat_coef_y[1] + position.y,
                    last_x * mat_coef_x[2] + last_y *
                    mat_coef_y[2] + position.z
                )
            )
            vertices.append((
                x * mat_coef_x[0] + y * mat_coef_y[0] + position.x,
                x * mat_coef_x[1] + y * mat_coef_y[1] + position.y,
                x * mat_coef_x[2] + y * mat_coef_y[2] + position.z
            )
            )

        last_x = x
        last_y = y
    return vertices