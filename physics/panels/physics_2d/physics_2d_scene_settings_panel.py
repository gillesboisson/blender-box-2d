
import bpy
from ...utils import physics_2d_enabled_on_mesh



class ThreePhysics2DSceneSettingsPanel(bpy.types.Panel):
    
    bl_idname = 'VIEW3D_PT_three_physics_2D_scene_settings_panel'
    bl_label = 'Three physics'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    
    def draw(self, context):
        scene = context.scene
        prop = scene.three_physics
        layout = self.layout    
        layout.separator(factor=0.5)
        col = layout.column()
        col.prop(prop,'physics_mode')
        col.separator(factor=2)
        if prop.physics_mode == "2d":
            row = col.row()
            row.prop(prop,'physics_2d_gravity')
            col.prop(prop,'physics_2d_orientation')
            col.prop(prop,'physics_2d_display_shape')


from bpy.utils import register_class, unregister_class

def register_physics_scene_panels() -> None:
    register_class(ThreePhysics2DSceneSettingsPanel)


def unregister_physics_scene_panels() -> None:
    unregister_class(ThreePhysics2DSceneSettingsPanel)