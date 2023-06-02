
from .cylinder_widget import CylinderWidget
from .box_widget import BoxWidget
from .sphere_widget import SphereWidget


from bpy.types import (
    GizmoGroup,
)

class RigidBodyWidgetGroup(GizmoGroup):
    bl_idname = "OBJECT_GGT_light_test"
    bl_label = "Test Light Widget"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    static_color = (0.5,1.0,0.5)
    dynamic_color = (0.5,0.5,1.0)
    ob = None

    @classmethod
    def poll(cls, context):
        ob = context.object
        return (ob and ob.type == 'MESH' and hasattr(ob,"data") and hasattr(ob.data,"three_rigid_body_3d") and ob.data.three_rigid_body_3d.enabled)

    def update_prop_targets(self, context):
        ob = context.object

        self.cylinder_gizmo.target_set_prop("radius", ob.data.three_rigid_body_3d, "shape_radius")
        self.cylinder_gizmo.target_set_prop("length", ob.data.three_rigid_body_3d, "shape_length")
        self.cylinder_gizmo.target_set_prop("translation", ob.data.three_rigid_body_3d, "shape_translation")

        self.box_gizmo.target_set_prop("scale", ob.data.three_rigid_body_3d, "shape_box_scale")
        self.box_gizmo.target_set_prop("translation", ob.data.three_rigid_body_3d, "shape_translation")

        self.sphere_gizmo.target_set_prop("radius", ob.data.three_rigid_body_3d, "shape_radius")
        self.sphere_gizmo.target_set_prop("translation", ob.data.three_rigid_body_3d, "shape_translation")

    def setup(self, context):
        # Assign the 'offset' target property to the light energy.
        ob = context.object
        cylinder_gz = self.gizmos.new(CylinderWidget.bl_idname)
        cylinder_gz.use_draw_modal = True
        self.cylinder_gizmo = cylinder_gz

        box_gz = self.gizmos.new(BoxWidget.bl_idname)
        box_gz.use_draw_modal = True
        self.box_gizmo = box_gz

        
        sphere_gz = self.gizmos.new(SphereWidget.bl_idname)        
        sphere_gz.use_draw_modal = True
        self.sphere_gizmo = sphere_gz
       
        self.update_prop_targets(context)

    
    

    def draw_prepare(self, context):
        ob = context.object

        
        

        if(ob.data.three_rigid_body_3d.mass == 0):
            color = self.static_color
        else:
            color = self.dynamic_color

        self.sphere_gizmo.color =  self.cylinder_gizmo.color = self.box_gizmo.color = color
        self.sphere_gizmo.color_highlight =  self.cylinder_gizmo.color_highlight = self.box_gizmo.color_highlight = color

        self.sphere_gizmo.hide = ob.data.three_rigid_body_3d.shape_type != 'sphere'
        self.cylinder_gizmo.hide = ob.data.three_rigid_body_3d.shape_type != 'cylinder'
        self.box_gizmo.hide = ob.data.three_rigid_body_3d.shape_type != 'box'



        self.cylinder_gizmo.target_orientation = ob.data.three_rigid_body_3d.shape_orientation

    def refresh(self, context):
        ob = context.object

        if(ob != self.ob):
            self.ob = ob
            self.update_prop_targets(context)

        self.cylinder_gizmo.matrix_basis = ob.matrix_basis
        self.sphere_gizmo.matrix_basis = ob.matrix_basis
        self.box_gizmo.matrix_basis = ob.matrix_basis

       

