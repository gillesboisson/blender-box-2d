from math import cos, pi, acos

import bpy

from mathutils import Matrix, Vector

from bpy.types import (Operator, Context)
from bpy.props import *
from .....utils.plan import get_plan_matrix

from ....utils import physics_2d_can_edit_prismatic_joint, display_joint_gizmos, display_joint, physics_2d_enabled_and_mesh_selected
from .physics_2d_base_limit_joint_edit_gizmo import Physics2DBaseLimitJointEditGizmo
from ...widgets.joints.physics_2d_prismatic_anchor_move_widget import Physics2DPrismaticAnchorMoveWidget
from ...widgets.joints.physics_2d_prismatic_axe_widget import Physics2DPrismaticAxeWidget
from ...widgets.joints.physics_2d_axe_rotation_widget import Physics2DAxeRotationWidget
from ...widgets.joints.physics_2d_axe_limit_widget import Physics2DAxeLimitWidget
from ...widgets.joints.physics_2d_axe_widget import Physics2DAxeWidget

class Physics2DPrismaticJointEditGizmo(Physics2DBaseLimitJointEditGizmo):
    bl_idname = "VIEW3D_GT_physics_2d_prismatic_joint_edit_gizmo"
    bl_label = "Physics 2D Prismatic Joint Edit Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}


    @classmethod
    def poll(cls, context):
        res = physics_2d_enabled_and_mesh_selected(context)  and display_joint(context)
        return res

    def get_joint_props(self, context):
        joints = list()


        for ob in bpy.data.objects:
            if hasattr(ob,"physics_2d_joints") and hasattr(ob.physics_2d_joints,"prismatic_joints"):
                for joint in ob.physics_2d_joints.prismatic_joints:
                    joints.append(joint)     

        return joints
    

    def anchor_gizmo_name_a(self):
        return Physics2DPrismaticAnchorMoveWidget.bl_idname
    
