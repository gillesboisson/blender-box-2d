

from math import pi
from ..utils.vertices import tuple_2_to_vec_3
from mathutils import Matrix, Vector

def physics_2d_enabled(context):
    ob = context.object
    return ob and ob.type == "MESH" and ob.data != None and ob.data.three_rigid_body_2d != None and context.scene.three_physics.physics_mode == '2d'




def physics_2d_enabled_on_mesh(context):
    return physics_2d_enabled(context) and context.object.data.three_rigid_body_2d.enabled == True

def physics_2d_can_edit_square_shape(context):
    return physics_2d_enabled_on_mesh(context) and context.object.data.three_rigid_body_2d.shape.shape_type == 'box'



def get_shape_local_matrix(context, shape):
    face_orientation = context.scene.three_physics.physics_2d_orientation

    shape_position_3d = tuple_2_to_vec_3(face_orientation, shape.shape_position)
    shape_angle = shape.shape_angle / 180 * pi



    shape_mat = Matrix.Translation(shape_position_3d) 
    shape_mat = shape_mat @ Matrix.Rotation(shape_angle, 4, face_orientation)

    return shape_mat


    