import bpy
from bpy.types import Context

from ..utils import physics_2d_enabled_on_mesh

class ThreePhysics2DBodyShapePanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_three_physics_2D_body_shape_panel'
    bl_label = 'Shape'
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
        col = layout.column(align=True)
        layout.use_property_split = True
        layout.use_property_decorate = False



        row = col.row()

        row.prop(prop.shape,'shape_position')
        col.prop(prop.shape,'shape_angle')
        col.separator(factor=2)
        col.prop(prop.shape,'friction')
        col.prop(prop.shape,'restitution')
        col.prop(prop.shape,'density')
        col.prop(prop.shape,'sensor')
        col.separator(factor=2)

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

        if prop.shape.shape_type == 'circle':
            col.prop(prop.shape,'shape_radius')


        if prop.shape.shape_type == 'polygon':
            
            # col.operator("physics_2d.physics_create_shape_poly", icon='ADD')
            
            for i in range(len(prop.shape.shape_polygon_vertices)):
                row = col.row()
                row.prop(prop.shape.shape_polygon_vertices[i],'pos', text="Vertex "+str(i))
                # row.operator("three_physics_2d.remove_shape_vertex", text="", icon='REMOVE').vertex_index = i
                # row.operator("three_physics_2d.edit_shape_vertex", text="", icon='HANDLE_VECTOR').vertex_index = i

        else:
            self.bl_parent_id = 'None'