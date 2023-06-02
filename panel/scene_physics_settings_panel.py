
import bpy
import gpu
import mathutils
from gpu_extras.batch import batch_for_shader
from bpy.props import IntProperty

from ..props.physics_2d_body_props import RigidBody2DPropertyGroup


class ThreePhysics2DScenePanel(bpy.types.Panel):
    
    bl_idname = 'VIEW2D_PT_three_physics_2D_scene_panel'
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


from bpy.utils import register_class, unregister_class

def register_physics_scene_panels() -> None:
    register_class(ThreePhysics2DScenePanel)


def unregister_physics_scene_panels() -> None:
    unregister_class(ThreePhysics2DScenePanel)