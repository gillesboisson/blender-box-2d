
import bpy
import gpu
import mathutils
from gpu_extras.batch import batch_for_shader

from ..props.entity_props import ThreeEntityPropertyGroup

class ThreeEntityPanel(bpy.types.Panel):
    
    bl_idname = 'VIEW3D_PT_entity_panel'
    bl_label = 'Entity du gilles'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Three"
    
    @classmethod
    def poll(cls, context: 'Context'):
        return context.active_object != None 


    def draw(self, context): 


        obj = context.active_object; 


        prop = obj.three_entity
        

        layout = self.layout    
    
        layout.separator(factor=0.5)
        col = layout.column()
        row = col.row()
        row.prop(prop,'static')
        col = layout.column()
        row = col.row()
        row.prop(prop,'cast_shadow')
        col = layout.column()
        row = col.row()
        row.prop(prop,'layer_mask')
            
            
                

    
                


