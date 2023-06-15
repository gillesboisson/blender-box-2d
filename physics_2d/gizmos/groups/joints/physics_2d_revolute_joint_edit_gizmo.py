from math import acos
from bpy.props import *
from mathutils import Matrix, Vector
from .....utils.plan import get_plan_matrix

from ....utils import physics_2d_can_edit_revolute_joint, display_joint_gizmos, display_joint
from .physics_2d_joint_edit_gizmo import Physics2DJointEditGizmo
from ...widgets.joints.physics_2d_revolute_anchor_widget import Physics2DRevoluteAnchorMoveWidget
from ...widgets.joints.physics_2d_distance_widget import Physics2DDistanceWidget

class Physics2DRevoluteJointEditGizmo(Physics2DJointEditGizmo):
    bl_idname = "VIEW3D_GT_physics_2d_revolute_joint_edit_gizmo"
    bl_label = "Physics 2D Revolute Joint Edit Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}


    @classmethod
    def poll(cls, context):
        res = physics_2d_can_edit_revolute_joint(context) and display_joint(context)
        return res

    def setup(self, context):
        self.joint_distance_widgets = list()

        return super().setup(context)

    def refresh_joint_widget(self, context, joint, ind_joint, len_anchors_widgets, anchor_gizmo_name_a, anchor_gizmo_name_b):

        if ind_joint >= len(self.joint_distance_widgets):
            distance_widget = self.gizmos.new(Physics2DDistanceWidget.bl_idname)
            self.joint_distance_widgets.append(distance_widget)
            distance_widget.use_draw_modal = True
            # draw scale is handle partially as it represented real distance between anchors
            distance_widget.use_draw_scale = False
            

        else:
            distance_widget = self.joint_distance_widgets[ind_joint]

        distance_widget.color = 1, 0.5, 0.5
        distance_widget.color_highlight = distance_widget.color

        distance_widget.target_set_prop('anchor_a', joint,"anchor_a")
        distance_widget.target_set_prop('anchor_b', joint,"anchor_b")
        distance_widget.target_set_prop('display_joint_gizmos',context.scene.three_physics.physics_2d_viewport_settings,'display_joint_gizmos')

        super().refresh_joint_widget(context, joint, ind_joint, len_anchors_widgets, anchor_gizmo_name_a, anchor_gizmo_name_b)


    def remove_joint_widgets(self, context, nb_joint, len_anchors_widgets):
    
        len_widgets = len(self.joint_distance_widgets)
        for ind_del in range(nb_joint, len_widgets):
            gz = self.joint_distance_widgets[ind_del]
            self.gizmos.remove(gz)
            self.joint_distance_widgets.remove(gz)
        
        super().remove_joint_widgets(context, nb_joint, len_anchors_widgets)


    def update_widget_matrix(
            self,
            context,
            joint_ind: int,
            joint,
            orientation_mat: Matrix,
            anchor_a,
            anchor_b,
            anchor_a_world_mat: Matrix,
            anchor_b_world_mat: Matrix
    ):
        super().update_widget_matrix(context,joint_ind, joint, orientation_mat, anchor_a, anchor_b, anchor_a_world_mat, anchor_b_world_mat)

        plan_mat = get_plan_matrix(orientation_mat).inverted()

        object_a_world_pos = (anchor_a_world_mat @ plan_mat).to_translation()
        object_b_world_pos = (anchor_b_world_mat @ plan_mat).to_translation()

        
        zoom = context.space_data.region_3d.view_distance
        axis = Vector(object_b_world_pos - object_a_world_pos)

        len = axis.length
        axis = axis.normalized()


        angle = acos(axis.x)
        if axis.y < 0:
            angle = -angle

        # distance is scale based on distance between anchors on X axis and based on view zoom
        scale_mat = Matrix.Scale(len, 4, (1, 0, 0)) @ Matrix.Scale(zoom * 0.005, 4, (0, 1, 0))
        
        rot_mat = Matrix.Rotation(angle, 4, 'Z')
        distance_mat = rot_mat @ scale_mat
        distance_widget = self.joint_distance_widgets[joint_ind]
        distance_widget.matrix_basis = anchor_a_world_mat @ distance_mat @ orientation_mat

        #set limit widget color based on joint limit matching length
        if len < 0.05:
            distance_widget.Hide = True
        else:
            distance_widget.Hide = False
            

    def get_joint_props(self, context):
        return context.scene.three_physics.physics_2d_joints.revolute_joints
    

    def anchor_gizmo_name_a(self):
        return Physics2DRevoluteAnchorMoveWidget.bl_idname
    


