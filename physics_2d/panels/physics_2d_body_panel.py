import bpy

from ..utils import physics_2d_enabled_and_mesh_selected

class ThreePhysics2DBodyPanel(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_three_physics_2D_body_panel'
    bl_label = 'Box2D rigid body'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return physics_2d_enabled_and_mesh_selected(context)

    def draw(self, context):


        obj = context.active_object.data;

        prop = obj.three_rigid_body_2d
        layout = self.layout
        layout.prop(prop,'enabled', text="Enabled")