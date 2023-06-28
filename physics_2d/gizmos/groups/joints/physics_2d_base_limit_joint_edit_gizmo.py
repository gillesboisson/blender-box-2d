from math import cos, pi, acos


from mathutils import Matrix, Vector

from bpy.types import (Operator, Context)
from bpy.props import *
from .....utils.plan import get_plan_matrix

from ....utils import physics_2d_can_edit_prismatic_joint, display_joint_gizmos, display_joint, physics_2d_enabled_and_mesh_selected
from .physics_2d_joint_edit_gizmo import Physics2DJointEditGizmo
from ...widgets.joints.physics_2d_prismatic_anchor_move_widget import Physics2DPrismaticAnchorMoveWidget
from ...widgets.joints.physics_2d_prismatic_axe_widget import Physics2DPrismaticAxeWidget
from ...widgets.joints.physics_2d_axe_rotation_widget import Physics2DAxeRotationWidget
from ...widgets.joints.physics_2d_axe_limit_widget import Physics2DAxeLimitWidget
from ...widgets.joints.physics_2d_axe_widget import Physics2DAxeWidget

class Physics2DBaseLimitJointEditGizmo(Physics2DJointEditGizmo):


    

    def setup(self, context):
        self.joint_arrow_widgets = list()
        self.joint_axe_rotation_widgets = list()
        self.joint_axe_limit_widgets = list()

        super().setup(context)
        
    arrow_widget_name = Physics2DPrismaticAxeWidget.bl_idname
    arrow_widget_color = 0.8, 0.8, 0.8
    axe_rotation_widget_name = Physics2DAxeRotationWidget.bl_idname
    axe_rotation_widget_color = 0.8, 0.8, 0.8
    axe_limit_widget_name = Physics2DAxeLimitWidget.bl_idname
    axe_limit_widget_color = 0.8, 0.8, 0.8
    axe_error_widget_color = 1.0, 0.5, 0.5

    def refresh_joint_widget(self, context: Context, joint, ind_joint, anchor_gizmo_name):


        if ind_joint >= len(self.joint_axe_limit_widgets):
            axe_limit_widget = self.gizmos.new(self.axe_limit_widget_name)
            self.joint_axe_limit_widgets.append(axe_limit_widget)
            axe_limit_widget.use_draw_modal = True
            axe_limit_widget.use_draw_scale = False
        else:
            axe_limit_widget = self.joint_axe_limit_widgets[ind_joint]
        

        if(joint.lower > 0 or joint.upper < 0):
            axe_limit_widget.color = self.axe_error_widget_color
            axe_limit_widget.color_highlight = self.axe_error_widget_color
        else:
            axe_limit_widget.color = self.joint_color
            axe_limit_widget.color_highlight = self.joint_color

        axe_limit_widget.target_set_prop('direction', joint,"local_axis")
        axe_limit_widget.target_set_prop('display_joint_gizmos',context.scene.three_physics.physics_2d_viewport_settings,'display_joint_gizmos')
        axe_limit_widget.target_set_prop('enable_limit',joint,'enable_limit')
        axe_limit_widget.target_set_prop('lower',joint,'lower')
        axe_limit_widget.target_set_prop('upper',joint,'upper')

        axe_limit_widget.hide = not joint.enable_limit


        if ind_joint >= len(self.joint_arrow_widgets):
            arrow_widget = self.gizmos.new(self.arrow_widget_name)
            self.joint_arrow_widgets.append(arrow_widget)
            arrow_widget.use_draw_modal = True
            arrow_widget.scale_basis = 0.3
        else:
            arrow_widget = self.joint_arrow_widgets[ind_joint]
        
        if(joint.enable_limit):
            arrow_widget.color =  0.4, 0.4, 0.4
            arrow_widget.color_highlight = 0.4, 0.4, 0.4
        else:
            arrow_widget.color =  self.joint_color
            arrow_widget.color_highlight = self.joint_color
            
        arrow_widget.color_highlight = self.joint_color

        arrow_widget.target_set_prop('direction', joint,"local_axis")
        arrow_widget.target_set_prop('display_joint_gizmos',context.scene.three_physics.physics_2d_viewport_settings,'display_joint_gizmos')
        arrow_widget.target_set_prop('enable_limit',joint,'enable_limit')
        
        if ind_joint >= len(self.joint_axe_rotation_widgets):
            axe_rotation_widget = self.gizmos.new(self.axe_rotation_widget_name)
            self.joint_axe_rotation_widgets.append(axe_rotation_widget)
            axe_rotation_widget.use_draw_modal = True
            axe_rotation_widget.scale_basis = 0.3
        else:
            axe_rotation_widget = self.joint_axe_rotation_widgets[ind_joint]

        axe_rotation_widget.color = self.gizmo_color
        axe_rotation_widget.color_highlight = self.gizmo_color

        axe_rotation_widget.target_set_prop('axis', joint,"local_axis")
        axe_rotation_widget.target_set_prop('anchor_position', joint,"anchor_a")
        axe_rotation_widget.hide = not self.display_joint_gizmos
      
        super().refresh_joint_widget(context, joint, ind_joint, anchor_gizmo_name)

      

    def remove_joint_widgets(self, context, nb_joint):
        super().remove_joint_widgets(context, nb_joint)
        for ind_del in range(nb_joint, len(self.joint_arrow_widgets)):
            gz = self.joint_arrow_widgets[nb_joint]
            self.gizmos.remove(gz)
            self.joint_arrow_widgets.remove(gz)
        
        for ind_del in range(nb_joint, len(self.joint_axe_rotation_widgets)):
            gz = self.joint_axe_rotation_widgets[nb_joint]
            self.gizmos.remove(gz)
            self.joint_axe_rotation_widgets.remove(gz)

        for ind_del in range(nb_joint, len(self.joint_axe_limit_widgets)):
            gz = self.joint_axe_limit_widgets[nb_joint]
            self.gizmos.remove(gz)
            self.joint_axe_limit_widgets.remove(gz)

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
        # anchor_widget_b = self.anchors_widgets_b[joint_ind]


        plan_mat = get_plan_matrix(orientation_mat).inverted()

        anchor_world_2d_mat: Matrix = anchor_widget_a.matrix_basis @ plan_mat

        object_a_world_pos = (anchor_world_2d_mat).to_translation()
        object_invert_scale = anchor_world_2d_mat.to_scale()
        object_invert_scale.x = 1 / object_invert_scale.x
        object_invert_scale.y = 1 / object_invert_scale.y
        object_invert_scale.z = 1 / object_invert_scale.z


        anchor_world_2d_mat @= Matrix.Scale(object_invert_scale.x,4,Vector((1,0,0))) @ Matrix.Scale(object_invert_scale.y,4,Vector((0,1,0)))

        # object_b_world_pos = (anchor_widget_b.matrix_basis @ plan_mat).to_translation()

        object_a_world_pos_mat = Matrix.Translation(object_a_world_pos)
        # object_b_world_pos_mat = Matrix.Translation(object_b_world_pos)

        # get angle from joint local axis
        local_axis = Vector((joint.local_axis[0], joint.local_axis[1])).normalized()
        angle = acos(local_axis.x)
        
        if local_axis.y < 0:
            angle = -angle


        arrow_mat = Matrix.Rotation(angle, 4, 'Z')
        arrow_widget = self.joint_arrow_widgets[joint_ind]
        arrow_widget.matrix_basis = anchor_world_2d_mat @ arrow_mat

        axe_rotation_widget = self.joint_axe_rotation_widgets[joint_ind]
        axe_rotation_widget.matrix_basis = anchor_world_2d_mat @ arrow_mat

        axe_limit_widget = self.joint_axe_limit_widgets[joint_ind]
        axe_limit_widget.matrix_basis = anchor_world_2d_mat @ arrow_mat @ Matrix.Translation((joint.lower, 0, 0)) @ Matrix.Scale(joint.upper - joint.lower, 4, Vector((1,0,0)))
 