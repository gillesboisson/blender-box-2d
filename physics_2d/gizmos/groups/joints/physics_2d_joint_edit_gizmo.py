from bpy.types import Context, GizmoGroup
from mathutils import Matrix, Vector
from ....types import PlanDirection
from .....utils.plan import clamp_matrix_to_plan, get_plan_matrix


class Physics2DJointEditGizmo(GizmoGroup):

    def setup(self, context):
        self.anchors_widgets = list()
        self.joints = list()

        self.anchor_a_color = 0.8, 0.8, 0.8
        self.anchor_b_color = 0.8, 0.8, 0.8

        self.refresh_widgets(context)

        return

    def get_joint_props(self, context):
        return list()

    def anchor_gizmo_name_a(self):
        return ""
    def anchor_gizmo_name_b(self):
        return self.anchor_gizmo_name_a()

    def refresh_joint_widget(self, context: Context, joint, ind_joint, len_anchors_widgets, anchor_gizmo_name_a, anchor_gizmo_name_b):
        ind_anchor = ind_joint * 2
        if ind_anchor >= len_anchors_widgets:
            anchor_a_widget = self.gizmos.new(anchor_gizmo_name_a)
            self.anchors_widgets.append(anchor_a_widget)
            anchor_a_widget.use_draw_modal = True
            anchor_a_widget.scale_basis = 0.3
        else:
            anchor_a_widget = self.anchors_widgets[ind_anchor]

        anchor_a_widget.color = self.anchor_a_color
        anchor_a_widget.color_highlight = self.anchor_a_color
        anchor_a_widget.target_set_prop('anchor_position', joint,"anchor_a")
        anchor_a_widget.target_set_prop('display_joint_gizmo', context.scene.three_physics.physics_2d_viewport_settings,"display_joint_gizmos")

        ind_anchor += 1
        if ind_anchor >= len_anchors_widgets:
            anchor_b_widget = self.gizmos.new(anchor_gizmo_name_b)
            self.anchors_widgets.append(anchor_b_widget)
            anchor_b_widget.use_draw_modal = True
            anchor_b_widget.scale_basis = 0.3

        else:
            anchor_b_widget = self.anchors_widgets[ind_anchor]

        anchor_b_widget.color = self.anchor_b_color
        anchor_b_widget.color_highlight = self.anchor_b_color
        anchor_b_widget.target_set_prop('anchor_position', joint,"anchor_b")
        anchor_b_widget.target_set_prop('display_joint_gizmo', context.scene.three_physics.physics_2d_viewport_settings,"display_joint_gizmos")

    def remove_joint_widgets(self, context: Context, nb_joint, len_anchors_widgets):
        nb_anchors = nb_joint * 2
        for ind_del in range(nb_anchors, len_anchors_widgets):
            self.gizmos.remove(self.anchors_widgets[nb_anchors])

    def refresh_widgets(self, context: Context):
        len_anchors_widgets = len(self.anchors_widgets)
        ind_joint = 0

        joints = self.get_joint_props(context)
        ob = context.object

        self.joints.clear()

        anchor_gizmo_name_a = self.anchor_gizmo_name_a()
        anchor_gizmo_name_b = self.anchor_gizmo_name_b()
        for joint in joints:

            if (joint.body_a is not None and joint.body_b is not None and (ob == joint.body_a or ob == joint.body_b)) and self.joints.count(joint) == 0:

                self.joints.append(joint)
                self.refresh_joint_widget(context, joint, ind_joint, len_anchors_widgets, anchor_gizmo_name_a, anchor_gizmo_name_b)
                ind_joint+=1

        self.remove_joint_widgets(context, ind_joint, len_anchors_widgets)

    def refresh(self, context: Context):
        self.refresh_widgets(context)
        return

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
        anchor_a_widget = self.anchors_widgets[joint_ind * 2]
        anchor_a_widget.matrix_basis = anchor_a_world_mat 

        anchor_b_widget = self.anchors_widgets[joint_ind * 2 + 1]
        anchor_b_widget.matrix_basis = anchor_b_world_mat 
        

    def update_widgets_matrix(self, context: Context):
        plan_direction = context.scene.three_physics.physics_2d_orientation
        orientation_mat = get_plan_matrix(plan_direction)


        for joint_ind in range(len(self.joints)):
            joint = self.joints[joint_ind]
            if(joint.body_a is None or joint.body_b is None):
                continue

            
            ob_a = joint.body_a
            matrix_world = ob_a.matrix_world
            body_a_world_mat = clamp_matrix_to_plan(plan_direction, matrix_world)
            anchor_a = joint.anchor_a
            local_a_mat = Matrix.Translation(Vector((anchor_a[0],anchor_a[1],0.0)))
            anchor_a_world_mat = body_a_world_mat @ orientation_mat @ local_a_mat

            ob_b = joint.body_b
            matrix_world = ob_b.matrix_world
            body_b_world_mat = clamp_matrix_to_plan(plan_direction, matrix_world)
            anchor_b = joint.anchor_b
            local_b_mat = Matrix.Translation(Vector((anchor_b[0],anchor_b[1],0.0)))
            anchor_b_world_mat = body_b_world_mat @ orientation_mat @ local_b_mat

            self.update_widget_matrix(
                context,
                joint_ind,
                joint,
                orientation_mat,
                anchor_a,
                anchor_b,
                anchor_a_world_mat,
                anchor_b_world_mat,
                )




    def draw_prepare(self, context):
        self.update_widgets_matrix(context)
        return