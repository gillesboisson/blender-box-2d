from bpy.types import Context, GizmoGroup
from mathutils import Matrix, Vector
from ....types import PlanDirection
from .....utils.plan import clamp_matrix_to_plan, get_face_orientation_matrix, get_plan_matrix, get_plan_2d_vector


class Physics2DJointEditGizmo(GizmoGroup):

    # def anchor_b_enabled(self, context):
    #     return False
    
    def object_inv_scale(self, context: Context,matrix_world ):

        body_world_mat_scale = matrix_world.to_scale()
        inv_scale = Vector((1.0/body_world_mat_scale.x,1.0/body_world_mat_scale.y,1.0/body_world_mat_scale.z))
        scale_2d = get_plan_2d_vector(context.scene.three_physics.physics_2d_orientation, inv_scale)

        

        # inv_scale_mat = Matrix.Scale(inv_scale.x,4,Vector((1.0,0.0,0.0))) @ Matrix.Scale(inv_scale.y,4,Vector((0.0,1.0,0.0))) @ Matrix.Scale(inv_scale.z,4,Vector((0.0,0.0,1.0)))
        # inv_scale_mat @= orientation_mat
        return scale_2d
    
    def object_inv_scale_mat(self, context: Context,matrix_world ):

        inc_scale = self.object_inv_scale(context, matrix_world)

        return Matrix(((inc_scale.x,0,0,0),(0,inc_scale.y,0,0),(0,0,1,0),(0,0,0,1)))
    

    def setup(self, context):
        self.anchors_widgets = list()
        self.joints = list()
        self.gizmo_color = 0.2, 0.5, 0.7
        self.joint_color = 0.7, 0.9, 1.0
        self.anchor_color = self.gizmo_color
        # self.anchor_b_color = self.gizmo_color
        

        self.refresh_widgets(context)

        return
    
    def get_body_a(self, context):
        return context.object

    def get_joint_props(self, context):
        return list()

    def anchor_gizmo_name_a(self):
        return ""
    # def anchor_gizmo_name_b(self):
    #     return self.anchor_gizmo_name_a()

    def refresh_anchor_widget(self, context: Context, joint, ind_joint, anchor_widgets, anchor_gizmo_name, anchor_color, prop_name, ref_object = None):
        if(ind_joint >= len(anchor_widgets)):
            anchor_widget = self.gizmos.new(anchor_gizmo_name)
            anchor_widgets.append(anchor_widget)
            anchor_widget.use_draw_modal = True
            anchor_widget.scale_basis = 0.3
        else:
            anchor_widget = anchor_widgets[ind_joint]

        anchor_widget.reference_object = ref_object
        
        anchor_widget.color = anchor_color
        anchor_widget.color_highlight = anchor_color
        anchor_widget.target_set_prop('anchor_position', joint, prop_name)
        anchor_widget.target_set_prop('display_joint_gizmo', context.scene.three_physics.physics_2d_viewport_settings,"display_joint_gizmos")
        anchor_widget.hide = not self.display_joint_gizmos

    def remove_anchor_widget(self, context: Context,  anchor_widgets, len_joint):
        len_anchor_widget = len(anchor_widgets)
        for ind_del in range(len_joint, len_anchor_widget):
            gz = anchor_widgets[len_joint]
            self.gizmos.remove(gz)
            anchor_widgets.remove(gz)

    def refresh_joint_widget(self, context: Context, joint, ind_joint, anchor_gizmo_name):

        self.refresh_anchor_widget(context, joint, ind_joint, self.anchors_widgets, anchor_gizmo_name, self.anchor_color, "anchor_a")


    def remove_joint_widgets(self, context: Context, nb_joint):
        
        self.remove_anchor_widget(context, self.anchors_widgets, nb_joint)


    def refresh_widgets(self, context: Context):
        self.display_joint_gizmos = context.scene.three_physics.physics_2d_viewport_settings.display_joint_gizmos


        joints = self.get_joint_props(context)
        # self.joints = joints
        anchor_gizmo_name_a = self.anchor_gizmo_name_a()
        ind_joint = 0
        # for ind_joint in range(0,len(joints)):
        #     self.refresh_joint_widget(context, joints[ind_joint], ind_joint, anchor_gizmo_name_a)


         # ob = context.object
        self.joints = list()
        duplicates = set()
        anchor_gizmo_name_a = self.anchor_gizmo_name_a()
        # anchor_gizmo_name_b = self.anchor_gizmo_name_b()
        for joint in joints:
            for ob in context.selected_objects:
                if (joint not in duplicates and joint.body_a is not None and joint.body_b is not None and (ob == joint.body_a or ob == joint.body_b)):
                    duplicates.add(joint)
                    self.joints.append(joint)
                    self.refresh_joint_widget(context, joints[ind_joint], ind_joint, anchor_gizmo_name_a)
                    # self.refresh_joint_widget(context, joint, ind_joint, len_anchors_widgets, anchor_gizmo_name_a, anchor_gizmo_name_b)
                    ind_joint+=1
        # self.remove_joint_widgets(context, ind_joint, len_anchors_widgets)
            
        self.remove_joint_widgets(context, len(self.joints))

    def refresh(self, context: Context):
        self.refresh_widgets(context)
        return
    

    def update_anchor_matrix(self,context, orientation_mat, joint_ind,anchor,anchors_widgets, body_world_mat, scale_inv_mat):
        
        anchor_a_widget = anchors_widgets[joint_ind]
        anchor_a_widget.matrix_basis = body_world_mat @ orientation_mat @ Matrix.Translation(Vector((anchor[0],anchor[1],0.0))) @ scale_inv_mat
         

    def update_widget_matrix(
            self,
            context,
            joint_ind: int,
            joint,
            orientation_mat: Matrix,
            body_a_world_mat: Matrix,
            body_b_world_mat: Matrix,
    ):
        self.update_anchor_matrix(context,orientation_mat,  joint_ind,joint.anchor_a,self.anchors_widgets, body_a_world_mat, self.cached_object_a_inv_scale_mat)
        

    def update_widgets_matrix(self, context: Context):
        plan_direction = context.scene.three_physics.physics_2d_orientation
        orientation_mat = get_plan_matrix(plan_direction)
        # plan_mat = get_plan_matrix(plan_direction)

        for joint_ind in range(len(self.joints)):
            joint = self.joints[joint_ind]
            if(joint.body_b is None):
                continue
            
            body_a = joint.body_a
            matrix_world = body_a.matrix_world
            body_a_world_mat = clamp_matrix_to_plan(plan_direction, matrix_world)
            self.cached_object_a_inv_scale_mat = self.object_inv_scale_mat(context, matrix_world)    

            body_b = joint.body_b
            matrix_world = body_b.matrix_world
            body_b_world_mat = clamp_matrix_to_plan(plan_direction, matrix_world)
            self.cached_object_b_inv_scale_mat = self.object_inv_scale_mat(context, body_b.matrix_world)    
            
            self.update_widget_matrix(
                context,
                joint_ind,
                joint,
                orientation_mat,
                body_a_world_mat,
                body_b_world_mat
                )




    def draw_prepare(self, context):
        self.update_widgets_matrix(context)
        return