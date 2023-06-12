import bpy
from bpy.types import Context
from .physics_2d_scene_settings_panel import ThreePhysics2DSceneSettingsPanel

from ..utils import physics_2d_enabled

def draw_distance_joint_properties(layout, joint, ind):
    card = layout.box()
    op = card.operator("physics_2d.physics_delete_distance_joint", text="", icon='X')
    op.joint_index = ind

    col = card.column()
    col.prop(joint,'name') 
    col.prop(joint,'body_a')
    col.prop(joint,'body_b')
    row = col.row()
    row.prop(joint,'anchor_a')
    row = col.row()
    row.prop(joint,'anchor_b')
    col.separator(factor=2)
    col.prop(joint,'collide_connected')
    col.prop(joint,'length')
    col.prop(joint,'frequency')
    col.prop(joint,'damping_ratio')

class ThreePhysics2DSceneDistanceJointPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_three_physics_2D_scene_distance_joint_panel'
    bl_label = 'Distance joints'
    bl_parent_id = 'VIEW3D_PT_three_physics_2D_scene_settings_panel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    @classmethod
    def poll(cls, context: 'Context'):
        return physics_2d_enabled(context)
    
    def draw(self, context):
        scene = context.scene
        prop = scene.three_physics.physics_2d_joints.distance_joints
 
        layout = self.layout    
        
        for ind in range(len(prop)):
            joint = prop[ind]
            draw_distance_joint_properties(layout, joint, ind)

            


class ThreePhysics2DObjectDistanceJointPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_three_physics_2D_object_distance_joint_panel'
    bl_label = 'Distance joint'
    bl_parent_id = 'VIEW3D_PT_three_physics_2D_body_panel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    @classmethod
    def poll(cls, context: 'Context'):
        return physics_2d_enabled(context)
    
    def draw(self, context):
        scene = context.scene
        prop = scene.three_physics.physics_2d_joints.distance_joints

        layout = self.layout    
        
        for ind in range(len(prop)):
            joint = prop[ind]
            if joint.body_a == context.object or joint.body_b == context.object:
                draw_distance_joint_properties(layout, joint, ind)
