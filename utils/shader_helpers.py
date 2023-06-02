
import bpy
import gpu
from gpu_extras.batch import batch_for_shader
from .vertices import vertices2DToVertices

vert_out = gpu.types.GPUStageInterfaceInfo("three_vert_interface")
vert_out.smooth('VEC3', "pos")

shader_info = gpu.types.GPUShaderCreateInfo()
shader_info.push_constant('MAT4', "viewProjectionMatrix")
shader_info.push_constant('MAT4', "modelMatrix")
shader_info.push_constant('VEC4', "color")

shader_info.vertex_in(0, 'VEC3', "position")
shader_info.vertex_out(vert_out)
shader_info.fragment_out(0, 'VEC4', "FragColor")

shader_info.vertex_source(
    "void main()"
    "{"
    "  pos = position;"
    "  gl_Position = viewProjectionMatrix * modelMatrix * vec4(position, 1.0f);"
    "}"
)

shader_info.fragment_source(
    "void main()"
    "{"
    "  FragColor = color;"
    "}"
)

shader = gpu.shader.create_from_info(shader_info)
del vert_out
del shader_info


def setShaderUniforms(vp, modelMat, color):
    shader.uniform_float("viewProjectionMatrix", vp)
    shader.uniform_float("modelMatrix", modelMat)
    shader.uniform_float("color",color)

def drawPolyline(coords, color, modelMat):
    vp = bpy.context.region_data.perspective_matrix
    setShaderUniforms(vp, modelMat, color)
    batch = batch_for_shader(shader, 'LINE_STRIP', {"position": coords})
    batch.draw(shader)


def drawPolyline2D(vertices2d, color, orientation, modelMat):
    vp = bpy.context.region_data.perspective_matrix
    setShaderUniforms(vp, modelMat, color)
    coords = vertices2DToVertices(vertices2d, orientation)
    batch = batch_for_shader(shader, 'LINE_STRIP', {"position": coords})
    batch.draw(shader)




