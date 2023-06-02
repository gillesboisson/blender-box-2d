import bpy, blf, gpu, bgl
from bgl import *
from gpu_extras.batch import batch_for_shader





cube_vertices = (
    ( -1.0, -1.0,  1.0),
    ( 1.0, -1.0,  1.0),
    ( 1.0,  1.0,  1.0),
    (-1.0,  1.0,  1.0),
    # back
    (-1.0, -1.0, -1.0),
    ( 1.0, -1.0, -1.0),
    ( 1.0,  1.0, -1.0),
    (-1.0,  1.0, -1.)
)

cube_indices = (
    # front
    (0, 1, 2),
    (2, 3, 0),
    # right
    (1, 5, 6),
    (6, 2, 1),
    # back
    (7, 6, 5),
    (5, 4, 7),
    # left
    (4, 0, 3),
    (3, 7, 4),
    # bottom
    (4, 5, 1),
    (1, 0, 4),
    # top
    (3, 2, 6),
    (6, 7, 3)
)


(
    (-0.5, -0.5, -0.5), (+0.5, -0.5, -0.5),
    (-0.5, +0.5, -0.5), (+0.5, +0.5, -0.5),
    (-0.5, -0.5, +0.5), (+0.5, -0.5, +0.5),
    (-0.5, +0.5, +0.5), (+0.5, +0.5, +0.5))


color_3d_shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
cube_batch = batch_for_shader(color_3d_shader, 'TRIS', {"pos": cube_vertices}, indices=cube_indices)


def draw_box(mat, color=(1,0,0,1)):
    color_3d_shader.bind()
    color_3d_shader.uniform_float("color", color)
    gpu.matrix.load_matrix
    glEnable(GL_BLEND)
    cube_batch.draw(color_3d_shader)
    glDisable(GL_BLEND)



def draw_quad(vertices=[], color=(1,1,1,1)):

    indices = [(0, 1, 2), (1, 2, 3)]
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
    shader.bind()
    shader.uniform_float("color", color)
    glEnable(GL_BLEND)
    batch.draw(shader)
    glDisable(GL_BLEND)
    
    del shader
    del batch


def draw_text(text,x,y,size=12, color=(1,1,1,1)):
    dpi = bpy.context.preferences.system.dpi
    font = 0
    blf.size(font, size, int(dpi))
    blf.color(font, *color)
    blf.position(font,x,y,0)
    blf.draw(font, text)

def get_blf_text_dimensions(text, size):
    '''Return dimension of text caption using blf API'''

    dpi = bpy.context.preferences.system.dpi
    blf.size(0, size, dpi)
    return blf.dimensions(0, str(text))
    

