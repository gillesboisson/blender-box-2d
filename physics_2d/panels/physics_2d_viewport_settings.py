
import bpy

from ..utils import physics_2d_enabled



class ThreePhysics2DViewportSettingsPanel(bpy.types.Panel):
    

    
    bl_idname = 'VIEW3D_PT_three_physics_2D_viewport_settings_panel'
    bl_label = 'View'
    # bl_category = "Physics 2D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Physics 2D"

    # @classmethod
    # def poll(cls, context):
    #     return physics_2d_enabled(context)
    
    def draw(self, context):
        scene = context.scene
        prop = scene.three_physics
        layout = self.layout

        row = layout.row()
        row.prop(prop.physics_2d_viewport_settings,'display_shape', text="Display shapes")
        if prop.physics_2d_viewport_settings.display_shape:
            row.prop(prop.physics_2d_viewport_settings, 'display_shape_gizmos', text="Shapes gizmos")

        row = layout.row()
        row.prop(prop.physics_2d_viewport_settings,'display_joint', text="Display joints")
        if prop.physics_2d_viewport_settings.display_joint:
            row.prop(prop.physics_2d_viewport_settings,'display_joint_gizmos', text="Joints gizmos")


        # layout.label(text="Shape")
        # col = layout.column()
        # col.prop(prop.physics_2d_viewport_settings,'display_shape_gizmos', text="Shape gizmos")
        # col.prop(prop.physics_2d_viewport_settings,'display_joint_gizmos', text="Joint gizmos")
        # layout.label(text="Display")
        # col = layout.column()
        # col.prop(prop.physics_2d_viewport_settings,'display_shape', text="Shape")
        # col.prop(prop.physics_2d_viewport_settings,'display_joint', text="Joint")

        
