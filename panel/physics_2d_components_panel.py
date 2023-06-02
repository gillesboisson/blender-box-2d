
import bpy
import gpu
import mathutils
from gpu_extras.batch import batch_for_shader
from bpy.props import IntProperty

from ..props.physics_2d_body_props import RigidBody2DPropertyGroup
        
class ThreePhysics2DBodySettingsComponentsPanel(bpy.types.Panel):
    
    bl_idname = 'VIEW2D_PT_three_physics_2D_body_settings_components_panel'
    bl_label = 'Body'
    bl_parent_id = 'VIEW2D_PT_three_physics_2D_body_components_panel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"




    @classmethod
    def poll(cls, context: 'Context'):
        return context.active_object.data.three_rigid_body_2d.enabled
    
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
           
    
class ThreePhysics2DBodyComponentsPanel(bpy.types.Panel):
    
    bl_idname = 'VIEW2D_PT_three_physics_2D_body_components_panel'
    bl_label = 'Three rigid body'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    
    @classmethod
    def poll(cls, context: 'Context'):
        return context.active_object.data != None and context.active_object.data.three_rigid_body_2d and context.scene.three_physics.physics_mode == '2d'

    # def draw_header(self, context):
    #     obj = context.active_object.data; 
    #     prop = obj.three_rigid_body_2d

    #     layout = self.layout
        
    #     layout.prop(prop,'enabled',text="")
        
    
    
    def draw(self, context):


        obj = context.active_object.data; 

        prop = obj.three_rigid_body_2d
        layout = self.layout  
        layout.prop(prop,'enabled', text="Enabled")
        

class ThreePhysics2DBodyShapeComponentsPanel(bpy.types.Panel):
    bl_idname = 'VIEW2D_PT_three_physics_2D_body_shape_components_panel'
    bl_label = 'Shape'
    bl_parent_id = 'VIEW2D_PT_three_physics_2D_body_components_panel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context: 'Context'):
        return context.active_object.data and context.active_object.data.three_rigid_body_2d and context.active_object.data.three_rigid_body_2d.enabled
    


    def draw(self, context):
        
        obj = context.active_object.data; 
        prop = obj.three_rigid_body_2d
        layout = self.layout    
        col = layout.column(align=True)
        layout.use_property_split = True
        layout.use_property_decorate = False

        

        row = col.row()
        row.prop(prop.shape,'shape_position')
        col.separator(factor=2)
        col.prop(prop.shape,'friction')
        col.prop(prop.shape,'restitution')
        col.prop(prop.shape,'density')
        col.prop(prop.shape,'sensor')
        col.separator(factor=2)
        
        # row = col.row()
        # subCol = row.column()
        # subCol = row.column()
        # row = col.row()
        row = col.row(align=True)
        col.prop(prop.shape,'filter_category_bits')
        col.prop(prop.shape,'filter_mask_bits')
        col.prop(prop.shape,'filter_group_index')

        col.separator(factor=2)

        col.prop(prop.shape,'shape_type')
        # box = col.box()
        if prop.shape.shape_type == 'box':
            row = col.row()
            row.prop(prop.shape,'shape_box_scale')
            row = col.row()
            row.prop(prop.shape,'shape_position')

        if prop.shape.shape_type == 'circle':
            col.prop(prop.shape,'shape_radius')
            col.prop(prop.shape,'shape_position')


        if prop.shape.shape_type == 'polygon':
            col.operator("physics_2d.add_shape_vertex", text="Add vertex", icon='ADD')
            for i in range(len(prop.shape.shape_polygon_vertices)):
                row = col.row()
                row.prop(prop.shape.shape_polygon_vertices[i],'pos', text="Vertex "+str(i))
                row.operator("physics_2d.remove_shape_vertex", text="", icon='REMOVE').vertex_index = i
                row.operator("physics_2d.edit_shape_vertex", text="", icon='HANDLE_VECTOR').vertex_index = i
            
        else:
            self.bl_parent_id = 'None'
            
    
            


    
                
from bpy.utils import register_class, unregister_class


def register_physics_2d_panels() -> None:
    register_class(ThreePhysics2DBodyComponentsPanel)
    register_class(ThreePhysics2DBodySettingsComponentsPanel)
    register_class(ThreePhysics2DBodyShapeComponentsPanel)


def unregister_physics_2d_panels() -> None:
    unregister_class(ThreePhysics2DBodyComponentsPanel)
    unregister_class(ThreePhysics2DBodySettingsComponentsPanel)
    unregister_class(ThreePhysics2DBodyShapeComponentsPanel)
