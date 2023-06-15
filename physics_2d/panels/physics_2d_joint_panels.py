
import bpy
from bpy.types import Context
from .physics_2d_scene_settings_panel import ThreePhysics2DSceneSettingsPanel

from ..utils import physics_2d_enabled




def draw_joint_edit_cards(joints,layout, draw_func):
    for ind in range(len(joints)):
        joint = joints[ind]
        card = layout.box()
        card.use_property_split = True
        card.use_property_decorate = False  # No animation.
        
        draw_func(card, joint, ind)


def draw_wheel_joint_properties(card, joint, ind):
    
    col = card.column()

    row = col.row()
    subcol = row.column()
    subcol.prop(joint,'name', text="Wheel joint") 
    subcol = row.column()
    op = subcol.operator("physics_2d.physics_delete_wheel_joint", text="", icon='X')
    op.joint_index = ind

    
    col.prop(joint,'body_a')
    col.prop(joint,'body_b')
    col.separator(factor=1)

    col.prop(joint,'anchor_a')
    col.prop(joint,'anchor_b')
    
    col.separator(factor=1)
    col.prop(joint,'collide_connected')

    col.prop(joint,'local_axis')
    
    col.separator(factor=1)
    col.prop(joint,'enable_motor')
    if joint.enable_motor:
        col.prop(joint,'motor_speed')
        col.prop(joint,'max_motor_torque')

    col.prop(joint,'frequency')
    col.prop(joint,'damping_ratio')

def draw_revolute_joint_properties(card, joint, ind):

    col = card.column()
    
    row = col.row()
    subcol = row.column()
    subcol.prop(joint,'name', text="Revolute joint") 
    subcol = row.column()
    op = subcol.operator("physics_2d.physics_delete_revolute_joint", text="", icon='X')
    op.joint_index = ind


    col.prop(joint,'body_a')
    col.prop(joint,'body_b')

    col.separator(factor=1)
    col.prop(joint,'anchor_a')
    col.prop(joint,'anchor_b')

    col.separator(factor=1)
    col.prop(joint,'collide_connected')
    col.prop(joint,'reference_angle')

    col.separator(factor=1)
    col.prop(joint,'enable_limit')
    if joint.enable_limit:
        col.prop(joint,'lower_angle')
        col.prop(joint,'upper_angle')

    col.separator(factor=1)
    col.prop(joint,'enable_motor')
    if joint.enable_motor:
        col.prop(joint,'motor_speed')
        col.prop(joint,'max_motor_torque')

def draw_prismatic_joint_properties(card, joint, ind):
    
    col = card.column()


    row = col.row()
    subcol = row.column()
    subcol.prop(joint,'name', text="Prismatic joint") 
    subcol = row.column()
    op = subcol.operator("physics_2d.physics_delete_prismatic_joint", text="", icon='X')
    op.joint_index = ind
    
    col.prop(joint,'body_a')
    col.prop(joint,'body_b')
    
    col.separator(factor=1)
    col.prop(joint,'anchor_a')
    col.prop(joint,'anchor_b')
    
    col.separator(factor=1)
    col.prop(joint,'collide_connected')
    col.prop(joint,'local_axis')
    
    col.separator(factor=2)
    col.prop(joint,'enable_limit')
    if joint.enable_limit:
        col.prop(joint,'lower')
        col.prop(joint,'upper')
    
    col.separator(factor=1)
    col.prop(joint,'enable_motor')
    if joint.enable_motor:
        col.prop(joint,'motor_speed')
        col.prop(joint,'max_motor_torque')

def draw_rope_joint_properties(card, joint, ind):

    col = card.column()
    
    row = col.row()
    subcol = row.column()
    subcol.prop(joint,'name', text="Rope joint") 
    subcol = row.column()
    op = subcol.operator("physics_2d.physics_delete_rope_joint", text="", icon='X')
    op.joint_index = ind

    col.prop(joint,'body_a')
    col.prop(joint,'body_b')

    col.separator(factor=1)
    col.prop(joint,'anchor_a')
    col.prop(joint,'anchor_b')

    col.separator(factor=1)
    col.prop(joint,'collide_connected')
    col.prop(joint,'length')

def draw_distance_joint_properties(card, joint, ind):

    col = card.column()


    row = col.row()
    subcol = row.column()
    subcol.prop(joint,'name', text="Distance joint") 
    subcol = row.column()
    op = subcol.operator("physics_2d.physics_delete_distance_joint", text="", icon='X')
    op.joint_index = ind



    col.prop(joint,'body_a')
    col.prop(joint,'body_b')
    col.separator(factor=1)

    col.prop(joint,'anchor_a')
    col.prop(joint,'anchor_b')
    col.separator(factor=1)
    col.prop(joint,'collide_connected')
    col.separator(factor=1)
    col.prop(joint,'length')
    col.prop(joint,'frequency')
    col.prop(joint,'damping_ratio')

class ThreePhysics2DSceneJointPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_three_physics_2D_scene_joint_panel'
    bl_label = 'Joints'
    bl_parent_id = 'VIEW3D_PT_three_physics_2D_scene_settings_panel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    @classmethod
    def poll(cls, context: 'Context'):
        return physics_2d_enabled(context)
    
    

    def draw(self, context):
        scene = context.scene
        wheel_joints = scene.three_physics.physics_2d_joints.wheel_joints

        layout = self.layout    
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        scene = context.scene

        draw_joint_edit_cards(scene.three_physics.physics_2d_joints.revolute_joints, layout, draw_revolute_joint_properties)
        
        draw_joint_edit_cards(scene.three_physics.physics_2d_joints.distance_joints, layout, draw_distance_joint_properties)

        draw_joint_edit_cards(scene.three_physics.physics_2d_joints.prismatic_joints, layout, draw_prismatic_joint_properties)

        draw_joint_edit_cards(scene.three_physics.physics_2d_joints.wheel_joints, layout, draw_wheel_joint_properties)

        draw_joint_edit_cards(scene.three_physics.physics_2d_joints.rope_joints, layout, draw_rope_joint_properties)
        


class ThreePhysics2DObjectJointPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_three_physics_2D_object_joint_panel'
    bl_label = 'Joints'
    bl_parent_id = 'VIEW3D_PT_three_physics_2D_body_panel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    @classmethod
    def poll(cls, context: 'Context'):
        return physics_2d_enabled(context)
    
    def draw(self, context):
        scene = context.scene
        
        layout = self.layout    
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.


        filtered_revolute_joints = list()
        for ind in range(len(scene.three_physics.physics_2d_joints.revolute_joints)):
            joint = scene.three_physics.physics_2d_joints.revolute_joints[ind]
            if joint.body_a == context.object or joint.body_b == context.object:
                filtered_revolute_joints.append(joint)

        draw_joint_edit_cards(filtered_revolute_joints, layout, draw_revolute_joint_properties)

        filtered_distance_joints = list()
        for ind in range(len(scene.three_physics.physics_2d_joints.distance_joints)):
            joint = scene.three_physics.physics_2d_joints.distance_joints[ind]
            if joint.body_a == context.object or joint.body_b == context.object:
                filtered_distance_joints.append(joint)

        draw_joint_edit_cards(filtered_distance_joints, layout, draw_distance_joint_properties)

        filtered_prismatic_joints = list()
        for ind in range(len(scene.three_physics.physics_2d_joints.prismatic_joints)):
            joint = scene.three_physics.physics_2d_joints.prismatic_joints[ind]
            if joint.body_a == context.object or joint.body_b == context.object:
                filtered_prismatic_joints.append(joint)

        draw_joint_edit_cards(filtered_prismatic_joints, layout, draw_prismatic_joint_properties)
        
        filtered_wheel_joints = list()
        for ind in range(len(scene.three_physics.physics_2d_joints.wheel_joints)):
            joint = scene.three_physics.physics_2d_joints.wheel_joints[ind]
            if joint.body_a == context.object or joint.body_b == context.object:
                filtered_wheel_joints.append(joint)

        draw_joint_edit_cards(filtered_wheel_joints, layout, draw_wheel_joint_properties)
        
        filtered_rope_joints = list()
        for ind in range(len(scene.three_physics.physics_2d_joints.rope_joints)):
            joint = scene.three_physics.physics_2d_joints.rope_joints[ind]
            if joint.body_a == context.object or joint.body_b == context.object:
                filtered_rope_joints.append(joint)

        draw_joint_edit_cards(filtered_rope_joints, layout, draw_rope_joint_properties)
