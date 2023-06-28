
import bpy

from ..utils import physics_2d_enabled



class ThreePhysics2DToolsPanel(bpy.types.Panel):
    

    
    bl_idname = 'VIEW3D_PT_three_physics_2D_tools_panel'
    bl_label = 'Tools'
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

        ob_props = context.object.data.three_rigid_body_2d
        row = layout.row()

        row.prop(ob_props,"enabled")

        layout.label(text="Create shapes")
        row = layout.row()
        row.operator("physics_2d.physics_create_shape_poly", text="Poly")
        row.operator("physics_2d.physics_create_circle_shape", text="Circle")
        row.operator("physics_2d.physics_create_box_shape", text="Box")


        layout.label(text="Create joints")
        col = layout.column(align=True)
        col.operator("physics_2d.physics_create_revolute_joint", text="Revolute")
        col.operator("physics_2d.physics_create_prismatic_joint", text="Prismatic")
        col.operator("physics_2d.physics_create_distance_joint", text="Distance")
        col.operator("physics_2d.physics_create_wheel_joint", text="Wheel")
        # col.operator("physics_2d.physics_create_rope_joint", text="Rope")
        

        
