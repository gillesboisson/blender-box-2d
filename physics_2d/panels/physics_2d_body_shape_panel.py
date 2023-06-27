import bpy
from bpy.types import Context

from ..utils import physics_2d_enabled_on_mesh

class ThreePhysics2DBodyShapesPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_three_physics_2D_body_shapes_panel'
    bl_label = 'Shapes'
    bl_parent_id = 'VIEW3D_PT_three_physics_2D_body_panel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context: 'Context'):
        return physics_2d_enabled_on_mesh(context)

        
    def draw(self, context):

        obj = context.active_object.data
        prop = obj.three_rigid_body_2d
        layout = self.layout
        
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        main_col = layout.column(align=True)

        for shape_ind in range(len(prop.shapes)):
            shape = prop.shapes[shape_ind]
            if shape_ind > 0:
                main_col.separator(factor=1)
            card = main_col.box()

            
            col = card.column(align=True)
            
            row = col.row()
            subcol = row.column()
            # subcol.prop(shape,'shape_type')
            subcol.label(text=shape.shape_type)
            subcol = row.column()
            op = subcol.operator("physics_2d.physics_delete_shape", text="", icon='X')
            op.shape_index = shape_ind

            col.separator(factor=2)

            col.prop(shape,'mass')
            col.separator(factor=2)

            col.prop(shape,'shape_position')
            if shape.shape_type != 'circle':
                col.prop(shape,'shape_angle')
                
            col.separator(factor=2)
            col.prop(shape,'friction')
            col.prop(shape,'restitution')
            col.prop(shape,'density')
            col.prop(shape,'sensor')
            col.separator(factor=2)

            col.prop(shape,'filter_category_bits')
            col.prop(shape,'filter_mask_bits')
            col.prop(shape,'filter_group_index')

            col.separator(factor=2)

            
            # box = col.box()
            if shape.shape_type == 'box':
                col.prop(shape,'shape_box_scale')

            if shape.shape_type == 'circle':
                col.prop(shape,'shape_radius')

            
            if shape.shape_type == 'polygon':
                
                
                for i in range(len(shape.shape_polygon_vertices)):
                    
                    card.use_property_split = False
                    col = card.column()
                    row = col.row()
                    
                    
                    row.prop(shape.shape_polygon_vertices[i],'pos', text="Vertex "+str(i))

        else:
            self.bl_parent_id = 'None'