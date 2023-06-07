from mathutils import Matrix, Vector
from .physics_2D_gizmo import Physics2DGizmo

from .widgets.square_fill_widget import SquareFillWidget
from .widgets.square_line_widget import SquareLineWidget

from bpy.types import (Context, GizmoGroup, Operator)
from bpy.props import *
import bpy

from ..utils.vertices import create_square_line_vertices, create_circle_line_vertices, create_polygon_line_vertices

from ..utils.draw import draw_polyline_2D

def can_edit_shape(context):
    ob = context.object
    return (ob and ob.type == 'MESH' and
        hasattr(ob,"data") and
        hasattr(ob.data,"three_rigid_body_2d") and
        ob.data.three_rigid_body_2d.enabled
    )



def draw_physics_2d_shape(self, context):
    if(can_edit_shape(context)):
        ob = context.object
        shape = ob.data.three_rigid_body_2d.shape
        orientation = context.scene.three_physics.physics_2d_orientation
        position = Vector(shape.shape_position)

        if(shape.shape_type == 'box'):
            scale = Vector(shape.shape_box_scale)
            vertices2D = create_square_line_vertices(scale, orientation, position)
            print(vertices2D)
        elif(shape.shape_type == 'circle'):
            vertices2D = create_circle_line_vertices(shape.shape_radius, orientation, 32, position)
        elif(shape.shape_type == 'polygon'):
            vertices2D = create_polygon_line_vertices(shape.shape_vertices, orientation, position)
        
        if(ob.data.three_rigid_body_2d.body_type == 'static'):
            color = (0.5,1.0,0.5)
        else:
            color = (0.5,0.5,1.0)
        
        draw_polyline_2D(vertices2D, color, orientation, ob.matrix_world)
        
    

class MoveShapePositionOperator(Operator):

    bl_idname = "three.move_shape_position"
    bl_label = "Move Shape Position"
    bl_description = "Move Shape Position"

    bl_options = {'REGISTER', 'UNDO'}
    
    position: FloatVectorProperty(name="Position", size=2, default=(0,0))


    @classmethod
    def poll(cls, context):
        return can_edit_shape(context)
    
    first_mouse_x: IntProperty()
    first_mouse_y: IntProperty()
    first_valueX: FloatProperty()
    first_valueY: FloatProperty()

    def modal(self, context, event):
        # print ("modal", event)
        if event.type == 'MOUSEMOVE':
            delta = self.first_mouse_x - event.mouse_x
            context.object.location.x = self.first_valueX + delta * 0.01
            delta = self.first_mouse_y - event.mouse_y
            context.object.location.y = self.first_valueY + delta * 0.01

        elif event.type == 'LEFTMOUSE':
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.object.location.x = self.first_valueX
            context.object.location.y = self.first_valueY
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.object:
            self.first_mouse_x = event.mouse_x
            self.first_mouse_y = event.mouse_y
            self.first_valueX = context.object.location.x
            self.first_valueY = context.object.location.y

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}
        


class Plane3DSquareGizmo(GizmoGroup):
    bl_idname = "THREE_PLANE_3D_SQUARE_GIZMO"
    bl_label = "Plane 3D Square Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}


    
    @staticmethod
    def my_target_operator(context):
        wm = context.window_manager
        op = wm.operators[-1] if wm.operators else None
        if isinstance(op, MoveShapePositionOperator):
            return op
        return None

    @classmethod
    def poll(cls, context):
        return can_edit_shape(context)

        
    gz = None
    def setup(self, context):

        gz = self.gizmos.new("GIZMO_GT_move_3d")

        def get_shape_position():
            op = Plane3DSquareGizmo.my_target_operator(context)
            # pos = op.position
        
            ob = context.object
            pos = ob.data.three_rigid_body_2d.shape.shape_position
            # face_orientation = context.scene.three_physics.physics_2d_orientation
            return Vector((pos[0],pos[1], 0.0))

        def set_shape_position(value):
            ob = context.object
            
            # face_orientation = context.scene.three_physics.physics_2d_orientation
            ob.data.three_rigid_body_2d.shape.shape_position = (value[0], value[1])

        
        def shape_range():
            return
       

        self.gz = gz

        gz.target_set_handler("offset", get=get_shape_position, set=set_shape_position, range=shape_range)
        
        # props = gz.target_set_operator("three.move_shape_position")

        gz.use_draw_value = True

        gz.color = 0.8, 0.8, 0.8
        gz.alpha = 0.5

        gz.color_highlight = 1.0, 1.0, 1.0
        gz.alpha_highlight = 1.0
        # gz.is_modal = True
        gz.scale_basis = 0.2

        self.gizmo_move = gz
        
        if(hasattr(self, "_handle")):
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        
        args = (self, context)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_physics_2d_shape, args, 'WINDOW', 'POST_VIEW')
    

        # self.matrix_basis = context.object.matrix_world



        return 
    
    def draw_prepare(self, context: Context):
        if self.gz is not None:
            self.gz.matrix_basis = context.object.matrix_world
       

    # def setup_widgets(self, context):
    #     fill_widget = self.gizmos.new(SquareFillWidget.bl_idname)
    #     # fill_widget.use_draw_offset_scale =True
    #     # fill_widget.use_draw_hover =True
    #     # fill_widget.use_draw_modal =True
    #     # fill_widget.select =True
    #     # fill_widget.is_modal = True
    #     # fill_widget.use_draw_modal = True
    #     self.fill_widget = fill_widget

    #     fill_widget.color = (0.5,0.5,0.7)
    #     fill_widget.color_highlight = (0.5,0.5,1.0)
    #     fill_widget.use_grab_cursor = True

    #     self.widgets.append(fill_widget)


    # def invoke(self, context, event):
    #     print("invoke")
    #     return {'RUNNING_MODAL'}
  

    
        
        





