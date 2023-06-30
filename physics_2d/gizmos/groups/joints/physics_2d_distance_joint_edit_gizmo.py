from math import acos
from bpy.props import *

import bpy

from bpy.types import Context

from mathutils import Matrix, Vector
from ...widgets.joints.physics_2d_axe_limit_widget import Physics2DAxeLimitWidget
from .....utils.plan import get_plan_2d_vector, get_plan_matrix

from ....utils import physics_2d_can_edit_distance_joint, display_joint_gizmos, display_joint, physics_2d_enabled_and_mesh_selected
from .physics_2d_joint_edit_gizmo import Physics2DJointEditGizmo
from ...widgets.joints.physics_2d_distance_anchor_widget import Physics2DDistanceAnchorMoveWidget
from ...widgets.joints.physics_2d_distance_widget import Physics2DDistanceWidget

class Physics2DDistanceJointEditGizmo(Physics2DJointEditGizmo):
    bl_idname = "VIEW3D_GT_physics_2d_distance_joint_edit_gizmo"
    bl_label = "Physics 2D Distance Joint Edit Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}


    @classmethod
    def poll(cls, context):
        res = physics_2d_enabled_and_mesh_selected(context) and display_joint(context)
        return res


    def setup(self, context):
        self.joint_distance_widgets = list()
        self.joint_limit_widgets = list()

        self.anchors_widgets_b = list()


        super().setup(context)
    def refresh_joint_widget(self, context: Context, joint, ind_joint, anchor_gizmo_name):
        
       
        if(ind_joint >= len(self.joint_distance_widgets)):
            distance_widget = self.gizmos.new(Physics2DDistanceWidget.bl_idname)
            self.joint_distance_widgets.append(distance_widget)
            distance_widget.use_draw_modal = True
            # draw scale is handle partially as it represented real distance between anchors
            distance_widget.use_draw_scale = False
        else:
            distance_widget = self.joint_distance_widgets[ind_joint]

        distance_widget.color = self.joint_color
        distance_widget.color_highlight = self.joint_color

        distance_widget.target_set_prop('anchor_a', joint,"anchor_a")
        distance_widget.target_set_prop('anchor_b', joint,"anchor_b")
        distance_widget.target_set_prop('display_joint_gizmos',context.scene.three_physics.physics_2d_viewport_settings,'display_joint_gizmos')


        if(ind_joint >= len(self.joint_limit_widgets)):
            limit_widget = self.gizmos.new(Physics2DAxeLimitWidget.bl_idname)
            self.joint_limit_widgets.append(limit_widget)
            limit_widget.use_draw_modal = True
            # draw scale is handle partially as it represented real distance between anchors
            limit_widget.use_draw_scale = False
            # distance_widget.scale_basis = 0.3
        else:
            limit_widget = self.joint_limit_widgets[ind_joint]


        limit_widget.color = self.joint_color
        limit_widget.color_highlight = self.joint_color

        limit_widget.target_set_prop('enable_limit', joint,"enable_limit")
        limit_widget.target_set_prop('display_joint_gizmos',context.scene.three_physics.physics_2d_viewport_settings,'display_joint_gizmos')
        limit_widget.hide = not joint.enable_limit

        super().refresh_joint_widget(context, joint, ind_joint, anchor_gizmo_name)

        self.refresh_anchor_widget(context, joint, ind_joint, self.anchors_widgets_b, self.anchor_gizmo_name_a(), self.anchor_color, "anchor_b", joint.body_b)



    def remove_joint_widgets(self, context: Context, nb_joint):
        super().remove_joint_widgets(context, nb_joint)
        self.remove_anchor_widget(context, self.anchors_widgets_b, nb_joint)

        len_widgets = len(self.joint_distance_widgets)

        for ind_del in range(nb_joint, len_widgets):
            gz = self.joint_distance_widgets[nb_joint]
            self.gizmos.remove(gz)
            self.joint_distance_widgets.remove(gz)

        len_widgets = len(self.joint_limit_widgets)

        for ind_del in range(nb_joint, len_widgets):
            gz = self.joint_limit_widgets[nb_joint]
            self.gizmos.remove(gz)
            self.joint_limit_widgets.remove(gz)



    def update_widget_matrix(
            self,
            context,
            joint_ind: int,
            joint,
            orientation_mat: Matrix,
            body_a_world_mat: Matrix,
            body_b_world_mat: Matrix,
    ):
        super().update_widget_matrix(context,joint_ind, joint, orientation_mat, body_a_world_mat, body_b_world_mat)

        anchor_widget_a = self.anchors_widgets[joint_ind]
        anchor_widget_b = self.anchors_widgets_b[joint_ind]

        self.update_anchor_matrix(context, orientation_mat, joint_ind,joint.anchor_b,self.anchors_widgets_b, body_b_world_mat, self.cached_object_b_inv_scale_mat)

        object_a_world_pos = (anchor_widget_a.matrix_basis @ orientation_mat).to_translation() 
        object_b_world_pos = (anchor_widget_b.matrix_basis @ orientation_mat).to_translation()

        zoom = context.space_data.region_3d.view_distance
        axis = Vector(object_b_world_pos - object_a_world_pos)
        axis_2d = get_plan_2d_vector(context.scene.three_physics.physics_2d_orientation,axis)

        len = axis_2d.length
        axis_2d = axis_2d.normalized()
        
        angle = acos(axis_2d.x)
        if axis_2d.y < 0:
            angle = -angle

        # distance is scale based on distance between anchors on X axis and based on view zoom
        scale_mat = Matrix.Scale(len, 4, (1, 0, 0)) @ Matrix.Scale(zoom * 0.01, 4, (0, 1, 0))
        rot_mat = Matrix.Rotation(angle, 4, 'Z')
        

        distance_mat = rot_mat @ scale_mat 
        distance_widget = self.joint_distance_widgets[joint_ind]
        distance_widget.matrix_basis = anchor_widget_a.matrix_basis @ distance_mat

        #     # len widget use same matrix as distance widget appart from using length target property
        len_min = joint.lower
        len_max = joint.upper

        #set limit widget color based on joint limit matching length
        if joint.enable_limit: 
            limit_matrix = anchor_widget_a.matrix_basis @ rot_mat 
            limit_matrix @= Matrix.Translation(Vector((len_min,0,0))) 
            limit_matrix @= Matrix.Scale(len_max -len_min, 4, (1, 0, 0)) 
            
            limit_widget = self.joint_limit_widgets[joint_ind]
            limit_widget.matrix_basis = limit_matrix @ self.cached_object_a_inv_scale_mat

            
            if (len >= len_min and len <= len_max):
                distance_widget.color = 0.5, 1.0, 0.5
                distance_widget.color_highlight = distance_widget.color
            else:
                distance_widget.color = 1, 0.5, 0.5
                distance_widget.color_highlight = distance_widget.color
        else:
            distance_widget.color = self.joint_color
            distance_widget.color_highlight = self.joint_color


                        
    def get_joint_props(self, context):

        joints = list()


        for ob in bpy.data.objects:
            if hasattr(ob,"physics_2d_joints") and hasattr(ob.physics_2d_joints,"distance_joints"):
                for joint in ob.physics_2d_joints.distance_joints:
                    joints.append(joint)                 


        return joints
        # return context.object.physics_2d_joints.distance_joints
        
    

    def anchor_gizmo_name_a(self):
        return Physics2DDistanceAnchorMoveWidget.bl_idname
    


