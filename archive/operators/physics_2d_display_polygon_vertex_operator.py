import bpy
from .actions import draw_poly_vertices, selectedObjectHasPhysics2DPolygonShape


class ThreePhysics2DDisplayPolygonVertexOperator(bpy.types.Operator):
    bl_idname = "three_physics_2d.display_shape_vertex"
    bl_label = "Display shape vertex"



    @classmethod
    def poll(cls, context):
        res = selectedObjectHasPhysics2DPolygonShape(context)
        return res
    def modal(self, context, event):

        if event.type == 'F8':
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            context.area.tag_redraw()
            return {'CANCELLED'}

        print(event.type)

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            # the arguments we pass the the callback
            args = (self, context)
            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_poly_vertices, args, 'WINDOW', 'POST_PIXEL')
            context.area.tag_redraw()

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}