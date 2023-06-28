from bpy.props import *
from .physics_2d_prismatic_joint_edit_gizmo import Physics2DPrismaticJointEditGizmo


from ....utils import physics_2d_can_edit_wheel_joint, display_joint
from .physics_2d_base_limit_joint_edit_gizmo import Physics2DBaseLimitJointEditGizmo

from ...widgets.joints.physics_2d_wheel_anchor_base_widget import Physics2DWheelAnchorBaseMoveWidget
from .physics_2d_base_limit_joint_edit_gizmo import Physics2DBaseLimitJointEditGizmo

from ...widgets.joints.physics_2d_distance_anchor_widget import Physics2DDistanceAnchorMoveWidget

class Physics2DWheelJointEditGizmo(Physics2DBaseLimitJointEditGizmo):
    bl_idname = "VIEW3D_GT_physics_2d_wheel_joint_edit_gizmo"
    bl_label = "Physics 2D Wheel Joint Edit Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}


    @classmethod
    def poll(cls, context):
        res = physics_2d_can_edit_wheel_joint(context) and display_joint(context)
        return res


    def get_joint_props(self, context):
        return context.object.physics_2d_joints.wheel_joints
    


    def anchor_gizmo_name_a(self):
        return Physics2DDistanceAnchorMoveWidget.bl_idname
    


