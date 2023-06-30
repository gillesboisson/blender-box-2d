

from math import pi
from ..utils.vertices import tuple_2_to_vec_3
from mathutils import Matrix, Vector

def physics_2d_enabled(context):
    return hasattr(context.scene,"three_physics") and context.scene.three_physics.physics_2d_enabled

def object_can_have_joint(context,ob):
    return ob and ob.type == "MESH" and ob.data != None and ob.data.three_rigid_body_2d != None and ob.data.three_rigid_body_2d.enabled 

# def physics_2d_can_edit_revolute_joint(context):
#     if not physics_2d_enabled_on_mesh(context):
#         return False
    
#     joints = context.scene.three_physics.physics_2d_joints.revolute_joints

#     # for joint in joints:
#     #     if joint.body_a == context.object or joint.body_b == context.object:
#     #         return True
        
#     return True

def physics_2d_can_edit_prismatic_joint(context):
    if not physics_2d_enabled_on_mesh(context):
        return False
    
    joints = context.scene.three_physics.physics_2d_joints.prismatic_joints

    # for joint in joints:
    #     if joint.body_a == context.object or joint.body_b == context.object:
    #         return True
        
    return True

def physics_2d_can_edit_distance_joint(context):
    if not physics_2d_enabled_on_mesh(context):
        return False
    
    # joints = context.scene.three_physics.physics_2d_joints.distance_joints

    # for joint in joints:
    #     if joint.body_a == context.object or joint.body_b == context.object:
    #         return True
    return True
        
    return False
def physics_2d_can_edit_wheel_joint(context):
    if not physics_2d_enabled_on_mesh(context):
        return False
    
    # joints = context.scene.three_physics.physics_2d_joints.wheel_joints

    # for joint in joints:
    #     if joint.body_a == context.object or joint.body_b == context.object:
    #         return True

    return True
        
    return False
def physics_2d_can_edit_rope_joint(context):
    if not physics_2d_enabled_on_mesh(context):
        return False
    
    # joints = context.scene.three_physics.physics_2d_joints.rope_joints

    # for joint in joints:
    #     if joint.body_a == context.object or joint.body_b == context.object:
    #         return True
        
    return True


def physics_2d_enabled_and_mesh_selected(context):
    ob = context.object
    return physics_2d_enabled(context) and ob and ob.type == "MESH" and ob.data != None


def physics_2d_enabled_on_mesh(context):
    ob = context.object
    return physics_2d_enabled(context) and ob and ob.type == "MESH" and ob.data != None and ob.data.three_rigid_body_2d != None and ob.data.three_rigid_body_2d.enabled == True


def display_shape(context):
    return context.scene.three_physics.physics_2d_viewport_settings.display_shape

def display_shape_gizmos(context):
    return context.scene.three_physics.physics_2d_viewport_settings.display_shape_gizmos

def display_joint_gizmos(context):
    return context.scene.three_physics.physics_2d_viewport_settings.display_joint_gizmos

def display_joint(context):
    return context.scene.three_physics.physics_2d_viewport_settings.display_joint

def get_snap_from_view_zoom_level(context):
    zoom = context.space_data.region_3d.view_distance
    start_zoom_snap = 1000
    
    for i in range(0, 20):
        if zoom > start_zoom_snap:
            return start_zoom_snap / 10
        start_zoom_snap /= 10


def get_shape_local_matrix(context, shape):
    face_orientation = context.scene.three_physics.physics_2d_orientation

    shape_position_3d = tuple_2_to_vec_3(face_orientation, shape.shape_position)
    shape_angle = shape.shape_angle / 180 * pi



    shape_mat = Matrix.Translation(shape_position_3d) 
    shape_mat = shape_mat @ Matrix.Rotation(shape_angle, 4, face_orientation)

    return shape_mat


    