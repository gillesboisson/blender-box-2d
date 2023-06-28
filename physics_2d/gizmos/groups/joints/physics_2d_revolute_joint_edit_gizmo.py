from bpy.props import *

from ....utils import display_joint, physics_2d_enabled_and_mesh_selected
from .physics_2d_joint_edit_gizmo import Physics2DJointEditGizmo
from ...widgets.joints.physics_2d_revolute_anchor_widget import Physics2DRevoluteAnchorMoveWidget

class Physics2DRevoluteJointEditGizmo(Physics2DJointEditGizmo):
    bl_idname = "VIEW3D_GT_physics_2d_revolute_joint_edit_gizmo"
    bl_label = "Physics 2D Revolute Joint Edit Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}


    @classmethod
    def poll(cls, context):
        res = physics_2d_enabled_and_mesh_selected(context) and display_joint(context)
        return res

            

    def get_joint_props(self, context):
        return context.object.physics_2d_joints.revolute_joints
    

    def anchor_gizmo_name_a(self):
        return Physics2DRevoluteAnchorMoveWidget.bl_idname
    


