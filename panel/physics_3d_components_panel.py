
import bpy
import gpu
import mathutils
from gpu_extras.batch import batch_for_shader

from ..props.physics_3d_body_props import RigidBody3DPropertyGroup

class ThreePhysics3DBodyComponentsPanel(bpy.types.Panel):
    
    bl_idname = 'VIEW3D_PT_three_physics_3D_body_components_panel'
    bl_label = 'Rigid body 3D'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Three"
    
    @classmethod
    def poll(cls, context: 'Context'):
        return context.active_object.data != None and context.scene.three_physics.physics_mode == '3d'

    def draw_header(self, context):
        obj = context.active_object.data; 
        prop = obj.three_rigid_body_3d

        layout = self.layout
        
        layout.prop(prop,'enabled',text="")
        
    
    
    def draw(self, context):


        obj = context.active_object.data; 

        prop = obj.three_rigid_body_3d
        

        layout = self.layout    
    
        if(prop.enabled):
            layout.separator(factor=0.5)
            col = layout.column()
            row = col.row()
            row.prop(prop,'mass')
            col = layout.column()
            row = col.row()
            row.prop(prop,'shape_type')
            row = col.row()
            row.prop(prop,'shape_translation')
            

            if prop.shape_type == 'box':
                row = col.row()
                row.prop(prop,'shape_box_scale')
            
           
        

            if prop.shape_type == 'cylinder' or prop.shape_type == 'sphere':
                row = col.row()
                row.prop(prop,'shape_radius')

            if prop.shape_type == 'cylinder':
                row = col.row()
                row.prop(prop,'shape_length')

                row = col.row()
                row.prop(prop,'shape_orientation')

            if prop.shape_type == 'mesh':
                row = col.row()
                row.prop(prop,'shape_mesh_object')
                if prop.shape_mesh_object == False:
                    row = col.row()
                    row.prop(prop,'shape_mesh')
                

class ThreePhysics2DBodyComponentsPanel(bpy.types.Panel):
    
    bl_idname = 'VIEW3D_PT_three_physics_2D_body_components_panel'
    bl_label = 'Rigid body 2D'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Three"
    
    @classmethod
    def poll(cls, context: 'Context'):
        return context.active_object.data != None 

    def draw_header(self, context):
        obj = context.active_object.data; 
        prop = obj.three_rigid_body_3d

        layout = self.layout
        
        layout.prop(prop,'enabled',text="")
        
    
    
    def draw(self, context):


        obj = context.active_object.data; 

        prop = obj.three_rigid_body_3d
        

        layout = self.layout    
    
        if(prop.enabled):
            layout.separator(factor=0.5)
            col = layout.column()
            row = col.row()
            row.prop(prop,'mass')
            col = layout.column()
            row = col.row()
            row.prop(prop,'shape_type')
            row = col.row()
            row.prop(prop,'shape_translation')
            if prop.shape_type == 'box':
                row = col.row()
                row.prop(prop,'shape_box_scale')
            
           
        

            if prop.shape_type == 'cylinder' or prop.shape_type == 'sphere':
                row = col.row()
                row.prop(prop,'shape_radius')

            if prop.shape_type == 'cylinder':
                row = col.row()
                row.prop(prop,'shape_length')

                row = col.row()
                row.prop(prop,'shape_orientation')

            if prop.shape_type == 'mesh':
                row = col.row()
                row.prop(prop,'shape_mesh_object')
                if prop.shape_mesh_object == False:
                    row = col.row()
                    row.prop(prop,'shape_mesh')
                

    
                


