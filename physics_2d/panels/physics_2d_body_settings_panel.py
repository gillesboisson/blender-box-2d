import bpy

from ..utils import physics_2d_enabled_on_mesh

class ThreePhysics2DBodySettingsPanel(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_three_physics_2D_body_settings_panel'
    bl_label = 'Body'
    bl_parent_id = 'VIEW3D_PT_three_physics_2D_body_panel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"




    @classmethod
    def poll(cls, context):
        return physics_2d_enabled_on_mesh(context)
    

   

    def draw(self, context):


        obj = context.active_object.data;

        prop = obj.three_rigid_body_2d

        layout = self.layout

        layout.separator(factor=0.5)
        col = layout.column()
        col.prop(prop,'mass')
        col.prop(prop,'body_type')
        col.prop(prop,'bullet')

        col.separator(factor=2)

        col.prop(prop,'fixed_rotation')
        col.prop(prop,'sleeping_allowed')
        col.prop(prop,'linear_damping')
        col.prop(prop,'angular_damping')

        col.separator(factor=2)

        col.prop(prop,'mass')
        col.prop(prop,'active')
        row = col.row()
        row.prop(prop,'linear_velocity')
        col.prop(prop,'angular_velocity')
        col.prop(prop,'awake')

        # self.draw_joints(layout, context)