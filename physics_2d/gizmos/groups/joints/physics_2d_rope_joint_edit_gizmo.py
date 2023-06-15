from math import acos
from bpy.props import *
from mathutils import Matrix, Vector
from .....utils.plan import get_plan_matrix

from ....utils import physics_2d_can_edit_rope_joint, display_joint_gizmos, display_joint
from .physics_2d_joint_edit_gizmo import Physics2DJointEditGizmo
from ...widgets.joints.physics_2d_distance_anchor_widget import Physics2DDistanceAnchorMoveWidget
from ...widgets.joints.physics_2d_distance_widget import Physics2DDistanceWidget
from ...widgets.joints.physics_2d_rope_arc_widget import Physics2DRopeArcWidget


class Physics2DRopeJointEditGizmo(Physics2DJointEditGizmo):
    bl_idname = "VIEW3D_GT_physics_2d_rope_joint_edit_gizmo"
    bl_label = "Physics 2D Rope Joint Edit Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}


    @classmethod
    def poll(cls, context):
        res = physics_2d_can_edit_rope_joint(context) and display_joint(context)
        return res


    def setup(self, context):
        self.joint_rope_widgets = list()
        self.joint_limit_widgets = list()
        self.joint_rope_arc_widgets = list()
        super().setup(context)

    def refresh_joint_widget(self, context, joint, ind_joint, len_anchors_widgets, anchor_gizmo_name_a, anchor_gizmo_name_b):

        if ind_joint >= len(self.joint_rope_widgets):
            rope_widget = self.gizmos.new(Physics2DDistanceWidget.bl_idname)
            self.joint_rope_widgets.append(rope_widget)
            rope_widget.use_draw_modal = True
            # draw scale is handle partially as it represented real rope between anchors
            rope_widget.use_draw_scale = False
            # rope_widget.scale_basis = 0.3
        else:
            rope_widget = self.joint_rope_widgets[ind_joint]

        rope_widget.color = self.anchor_a_color
        rope_widget.color_highlight = self.anchor_a_color

        rope_widget.target_set_prop('anchor_a', joint,"anchor_a")
        rope_widget.target_set_prop('anchor_b', joint,"anchor_b")
        rope_widget.target_set_prop('display_joint_gizmos',context.scene.three_physics.physics_2d_viewport_settings,'display_joint_gizmos')


        
        if ind_joint >= len(self.joint_limit_widgets):
            limit_widget = self.gizmos.new(Physics2DDistanceWidget.bl_idname)
            self.joint_limit_widgets.append(limit_widget)
            limit_widget.use_draw_modal = True
            # draw scale is handle partially as it represented real rope between anchors
            limit_widget.use_draw_scale = False
        else:
            limit_widget = self.joint_limit_widgets[ind_joint]

        limit_widget.color = self.anchor_a_color
        limit_widget.color_highlight = self.anchor_a_color

        limit_widget.target_set_prop('anchor_a', joint,"anchor_a")
        limit_widget.target_set_prop('anchor_b', joint,"anchor_b")

        if ind_joint >= len(self.joint_rope_arc_widgets):
            rope_arc = self.gizmos.new(Physics2DRopeArcWidget.bl_idname)
            self.joint_rope_arc_widgets.append(rope_arc)
            rope_arc.use_draw_modal = True
            rope_arc.use_draw_scale = False
        else:
            rope_arc = self.joint_rope_arc_widgets[ind_joint]

        rope_arc.color = self.anchor_a_color
        rope_arc.color_highlight = self.anchor_a_color

        rope_arc.target_set_prop('anchor_a', joint,"anchor_a")
        rope_arc.target_set_prop('anchor_b', joint,"anchor_b")





        super().refresh_joint_widget(context, joint, ind_joint, len_anchors_widgets, anchor_gizmo_name_a, anchor_gizmo_name_b)

    def remove_joint_widgets(self, context, nb_joint, len_widgets):
        super().remove_joint_widgets(context, nb_joint, len_widgets)
        len_widgets = len(self.joint_rope_widgets)
        for ind_del in range(nb_joint, len_widgets):
            self.gizmos.remove(self.joint_rope_widgets[nb_joint])

        len_widgets = len(self.joint_limit_widgets)
        for ind_del in range(nb_joint, len_widgets):
            self.gizmos.remove(self.joint_limit_widgets[nb_joint])

        len_widgets = len(self.joint_rope_arc_widgets)
        for ind_del in range(nb_joint, len_widgets):
            self.gizmos.remove(self.joint_rope_arc_widgets[nb_joint])



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

        # rope is scale based on rope between anchors on X axis and based on view zoom
        scale_mat = Matrix.Scale(len, 4, (1, 0, 0)) @ Matrix.Scale(zoom * 0.03, 4, (0, 1, 0))
        
        rot_mat = Matrix.Rotation(angle, 4, 'Z')
        rope_mat = rot_mat @ scale_mat
        rope_widget = self.joint_rope_widgets[joint_ind]
        rope_widget.matrix_basis = anchor_a_world_mat @ rope_mat @ orientation_mat

        # len widget use same matrix as rope widget appart from using length target property
        len_limit = joint.length
        scale_mat = Matrix.Scale(len_limit, 4, (1, 0, 0)) @ Matrix.Scale(zoom * 0.01, 4, (0, 1, 0))
        rope_mat = rot_mat @ scale_mat
        limit_widget = self.joint_limit_widgets[joint_ind]
        limit_widget.matrix_basis = anchor_a_world_mat @ rope_mat @ orientation_mat

        #set limit widget color based on joint limit matching length
       

        
        rope_arc_widget = self.joint_rope_arc_widgets[joint_ind]
        radius_scale = Matrix(((len_limit,0,0,0), (0,len_limit,0,0), (0,0,len_limit,0), (0,0,0,1)))
        rope_arc_widget.matrix_basis = anchor_a_world_mat @ orientation_mat @ radius_scale @ rot_mat


        if len-len_limit < 0.05:
            limit_widget.color = 0.5, 1.0, 0.5
            limit_widget.color_highlight = limit_widget.color
            rope_arc_widget.color = limit_widget.color
            rope_arc_widget.color_highlight = limit_widget.color
        else:
            limit_widget.color = 1, 0.5, 0.5
            limit_widget.color_highlight = limit_widget.color
            rope_arc_widget.color = limit_widget.color
            rope_arc_widget.color_highlight = limit_widget.color
                        
    def get_joint_props(self, context):
        return context.scene.three_physics.physics_2d_joints.rope_joints
        
    

    def anchor_gizmo_name_a(self):
        return Physics2DDistanceAnchorMoveWidget.bl_idname
    


