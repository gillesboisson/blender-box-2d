from math import acos
from bpy.props import *
from mathutils import Matrix, Vector

from ....utils import physics_2d_can_edit_wheel_joint, display_joint_gizmos, display_joint
from .physics_2d_joint_edit_gizmo import Physics2DJointEditGizmo
from ...widgets.joints.physics_2d_distance_anchor_widget import Physics2DDistanceAnchorMoveWidget
from ...widgets.joints.physics_2d_wheel_anchor_base_widget import Physics2DWheelAnchorBaseMoveWidget
from ...widgets.joints.physics_2d_prismatic_axe_widget import Physics2DPrismaticAxeWidget
from ...widgets.joints.physics_2d_axe_rotation_widget import Physics2DAxeRotationWidget
from ...widgets.joints.physics_2d_axe_widget import Physics2DAxeWidget

class Physics2DWheelJointEditGizmo(Physics2DJointEditGizmo):
    bl_idname = "VIEW3D_GT_physics_2d_wheel_joint_edit_gizmo"
    bl_label = "Physics 2D Wheel Joint Edit Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}


    @classmethod
    def poll(cls, context):
        res = physics_2d_can_edit_wheel_joint(context) and display_joint_gizmos(context) and display_joint(context)
        return res

    def get_joint_props(self, context):
        return context.scene.three_physics.physics_2d_joints.wheel_joints
    
    def setup(self, context):
        self.joint_arrow_widgets = list()
        self.joint_axe_rotation_widgets = list()
        self.joint_axe_error_widgets = list()
        super().setup(context)
        


    def refresh_widgets(self, context):
       
        self.arrow_widget_name = Physics2DPrismaticAxeWidget.bl_idname
        self.arrow_widget_color = 0.8, 0.8, 0.8
        self.axe_rotation_widget_name = Physics2DAxeRotationWidget.bl_idname
        self.axe_rotation_widget_color = 0.8, 0.8, 0.8
        self.axe_error_widget_name = Physics2DAxeWidget.bl_idname
        self.axe_error_widget_color = 1.0, 0.5, 0.5

        super().refresh_widgets(context)

    def refresh_joint_widget(self, context, joint, ind_joint, len_anchors_widgets, anchor_gizmo_name_a, anchor_gizmo_name_b):
        

        if ind_joint >= len(self.joint_arrow_widgets):
            arrow_widget = self.gizmos.new(self.arrow_widget_name)
            self.joint_arrow_widgets.append(arrow_widget)
            arrow_widget.use_draw_modal = True
            arrow_widget.scale_basis = 0.3
        else:
            arrow_widget = self.joint_arrow_widgets[ind_joint]
        
        arrow_widget.color = self.arrow_widget_color
        arrow_widget.color_highlight = self.arrow_widget_color

        arrow_widget.target_set_prop('direction', joint,"local_axis")

        if ind_joint >= len(self.joint_axe_rotation_widgets):
            axe_rotation_widget = self.gizmos.new(self.axe_rotation_widget_name)
            self.joint_axe_rotation_widgets.append(axe_rotation_widget)
            axe_rotation_widget.use_draw_modal = True
            axe_rotation_widget.scale_basis = 0.3
        else:
            axe_rotation_widget = self.joint_axe_rotation_widgets[ind_joint]

        axe_rotation_widget.color = self.axe_rotation_widget_color
        axe_rotation_widget.color_highlight = self.axe_rotation_widget_color

        axe_rotation_widget.target_set_prop('axis', joint,"local_axis")
        axe_rotation_widget.target_set_prop('anchor_position', joint,"anchor_a")

        if ind_joint >= len(self.joint_axe_error_widgets):
            axe_error_widget = self.gizmos.new(self.axe_error_widget_name)
            self.joint_axe_error_widgets.append(axe_error_widget)
            axe_error_widget.use_draw_modal = True
            axe_error_widget.use_draw_scale = False
        else:
            axe_error_widget = self.joint_axe_error_widgets[ind_joint]

        axe_error_widget.color = self.axe_error_widget_color
        axe_error_widget.color_highlight = self.axe_error_widget_color

        axe_error_widget.target_set_prop('direction', joint,"local_axis")

        super().refresh_joint_widget(context, joint, ind_joint, len_anchors_widgets, anchor_gizmo_name_a, anchor_gizmo_name_b)

    def remove_joint_widgets(self, context, nb_joint, len_anchors_widgets):
        super().remove_joint_widgets(context, nb_joint, len_anchors_widgets)
        for ind_del in range(nb_joint, len(self.joint_arrow_widgets)):
            self.gizmos.remove(self.joint_arrow_widgets[nb_joint])
        
        for ind_del in range(nb_joint, len(self.joint_axe_rotation_widgets)):
            self.gizmos.remove(self.joint_axe_rotation_widgets[nb_joint])

        for ind_del in range(nb_joint, len(self.joint_axe_error_widgets)):
            self.gizmos.remove(self.joint_axe_error_widgets[nb_joint])


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
        
        # get angle from joint local axis
        local_axis = Vector((joint.local_axis[0], joint.local_axis[1])).normalized()
        angle = acos(local_axis.x)
        
        if local_axis.y < 0:
            angle = -angle


        arrow_mat = Matrix.Rotation(angle, 4, 'Z')
        arrow_widget = self.joint_arrow_widgets[joint_ind]
        arrow_widget.matrix_basis = anchor_a_world_mat @ arrow_mat

        axe_rotation_widget = self.joint_axe_rotation_widgets[joint_ind]
        axe_rotation_widget.matrix_basis = anchor_a_world_mat @ arrow_mat

        # if anchors direction vector is not aligne to axe display a perpendicular axe as error
        inv_orientation_map = orientation_mat.inverted()

        anchor_ab_vector = (anchor_b_world_mat @ inv_orientation_map).translation - (anchor_a_world_mat @ inv_orientation_map).translation
        anchor_ab_vector = Vector((anchor_ab_vector.x, anchor_ab_vector.y))

        cross_vec = anchor_ab_vector.cross(local_axis)

        axe_error_widget = self.joint_axe_error_widgets[joint_ind]
        if(abs(cross_vec) > 0.01):

            # rotate pi / 2
            direction_vector = Vector((-local_axis.y, local_axis.x))

            angle = acos(direction_vector.x)
            if direction_vector.y < 0:
                angle = -angle
            
            axe_error_widget.hide = False

            axe_error_widget.matrix_basis = anchor_b_world_mat @ Matrix.Rotation(angle,4,"Z") @ Matrix.Scale(cross_vec,4, (1,0,0))
        else:
            axe_error_widget.hide = True
        

        

        
        
    

    def anchor_gizmo_name_b(self):
        return Physics2DDistanceAnchorMoveWidget.bl_idname
    
    def anchor_gizmo_name_a(self):
        return Physics2DWheelAnchorBaseMoveWidget.bl_idname
    


