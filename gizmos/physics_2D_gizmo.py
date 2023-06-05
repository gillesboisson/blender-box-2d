from bpy.types import GizmoGroup, Gizmo
from mathutils import Matrix, Vector

from ..utils.vertices import get_face_orientation_matrix






class Physics2DGizmo(GizmoGroup):

    def setup_widgets(self, context):
        return

    def setup(self, context):
        self.setup_widgets(context)
        self.draw_prepare_widgets(context)

    widgets = list()

    def update_transform(self, context):
        ob = context.object
        face_orientation = context.scene.three_physics.physics_2d_orientation

        shape_position = Vector((
            ob.data.three_rigid_body_2d.shape.shape_position[0],
            ob.data.three_rigid_body_2d.shape.shape_position[1],
            0.0
        ))

        translation = get_face_orientation_matrix(face_orientation) @ shape_position

        translation += ob.location

        mat = Matrix.Translation(translation)
        for widget in self.widgets:
            widget.matrix_basis = mat

    def draw_prepare_widgets(self, context):


        scene_physics_orientation = context.scene.three_physics.physics_2d_orientation

        if(not hasattr(self,'last_orientation') or self.last_orientation != scene_physics_orientation):
            self.last_orientation = scene_physics_orientation

            for widget in self.widgets:
                widget.orientation = scene_physics_orientation
                # if(hasattr(widget,"setup")):
                #     widget.setup()
                if(hasattr(widget,"updateShapes")):
                    widget.updateShapes(context, scene_physics_orientation)
                    
            self.last_orientation = scene_physics_orientation

            self.update_transform(context)



    def refresh_widgets(self, context):

        self.update_transform(context)


    def draw_prepare(self, context):
        self.draw_prepare_widgets(context)

    def refresh(self, context):
        self.refresh_widgets(context)