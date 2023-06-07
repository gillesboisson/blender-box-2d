
from .widgets.square_fill_widget import SquareFillWidget

from .widgets.circle_widget import CircleWidget
from .widgets.polygon_widget import PolygonWidget



from bpy.types import (
    GizmoGroup,
)


body_static_color = (0.5,1.0,0.5)
body_dynamic_color = (0.5,0.5,1.0)


class RigidBody2DWidgetGroup(GizmoGroup):
    bl_idname = "OBJECT_RIGID_BODY_2D_WIDGET_GROUP"
    bl_label = "Test Light Widget"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    
    ob = None

    @classmethod
    def poll(cls, context):
        ob = context.object
        return (ob and ob.type == 'MESH' and hasattr(ob,"data") and hasattr(ob.data,"three_rigid_body_2d") and ob.data.three_rigid_body_2d.enabled)

    def update_prop_targets(self, context):
        ob = context.object
        scene = context.scene

        # self.square_gizmo.target_set_prop("position", ob.data.three_rigid_body_2d.shape, "shape_position")
        # self.square_gizmo.target_set_prop("size", ob.data.three_rigid_body_2d.shape, "shape_box_scale")
       

        self.circle_gizmo.target_set_prop("position", ob.data.three_rigid_body_2d.shape, "shape_position")
        self.circle_gizmo.target_set_prop("radius", ob.data.three_rigid_body_2d.shape, "shape_radius")

        self.polygon_gizmo.target_set_prop("position", ob.data.three_rigid_body_2d.shape, "shape_position")
        # self.polygon_gizmo.target_set_prop("shape_vertices", ob.data.three_rigid_body_2d.shape, "shape_vertices")

    def setup(self, context):
        # Assign the 'offset' target property to the light energy.
        ob = context.object

        square_bz = self.gizmos.new(SquareFillWidget.bl_idname)
        square_bz.use_draw_modal = False
        self.square_gizmo = square_bz

        circle_bz = self.gizmos.new(CircleWidget.bl_idname)
        circle_bz.use_draw_modal = False
        self.circle_gizmo = circle_bz

        polygon_bz = self.gizmos.new(PolygonWidget.bl_idname)
        polygon_bz.use_draw_modal = False
        self.polygon_gizmo = polygon_bz
        if(hasattr(ob.data.three_rigid_body_2d.shape,"shape_polygon_vertices")):
            polygon_bz.vertices = ob.data.three_rigid_body_2d.shape.shape_polygon_vertices

        
       
        self.update_prop_targets(context)

    
    

    def draw_prepare(self, context):
        ob = context.object

        if(ob.data.three_rigid_body_2d.mass == 0 or ob.data.three_rigid_body_2d.body_type == 'static'):
            color = body_static_color
        else:
            color = body_dynamic_color

        
        self.square_gizmo.alpha = 0.5
        self.circle_gizmo.alpha_highlight = 0.9
        self.square_gizmo.color = color
        self.square_gizmo.color_highlight = color

        self.square_gizmo.hide = ob.data.three_rigid_body_2d.shape.shape_type != 'box' or True

        if(not hasattr(self,"square_gizmo.orientation") or context.scene.three_physics.physics_2d_orientation != self.square_gizmo.orientation ):
            self.square_gizmo.orientation = context.scene.three_physics.physics_2d_orientation
            # self.square_gizmo.setup()

       
        self.circle_gizmo.color = color
        self.circle_gizmo.color_highlight = color
        self.circle_gizmo.hide = ob.data.three_rigid_body_2d.shape.shape_type != 'circle'   

        if(not hasattr(self,"circle_gizmo.orientation") or context.scene.three_physics.physics_2d_orientation != self.circle_gizmo.orientation ):
            self.circle_gizmo.orientation = context.scene.three_physics.physics_2d_orientation
            self.circle_gizmo.setup()

        self.polygon_gizmo.color = color
        self.polygon_gizmo.color_highlight = color
        self.polygon_gizmo.hide = ob.data.three_rigid_body_2d.shape.shape_type != 'polygon'   

        if(not hasattr(self,"polygon_gizmo.orientation") or context.scene.three_physics.physics_2d_orientation != self.polygon_gizmo.orientation ):
            self.polygon_gizmo.orientation = context.scene.three_physics.physics_2d_orientation
            self.polygon_gizmo.setup()

        

    def refresh(self, context):
        ob = context.object
        if(ob != self.ob):
            self.ob = ob
            self.update_prop_targets(context)

        self.square_gizmo.matrix_basis = ob.matrix_basis
        self.circle_gizmo.matrix_basis = ob.matrix_basis
        self.polygon_gizmo.matrix_basis = ob.matrix_basis

       


