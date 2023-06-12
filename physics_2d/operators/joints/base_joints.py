

import bpy

from bpy.types import Context, Event

import bpy

from bpy.types import Context, Event

class Physics2DCreateJointOperator(bpy.types.Operator):

    def add_joint(self, context, event):
        return None

    def invoke(self, context: Context, event:Event):

        
        ob_with_bodies = list()
        
 
        for ob in context.selected_objects:
            if ob.data.three_rigid_body_2d != None and ob.data.three_rigid_body_2d.enabled == True:
                ob_with_bodies.append(ob)
                if len(ob_with_bodies) >= 2:
                    break

        if len(ob_with_bodies) < 2:
            # show a notification as 2 objects are requires
            self.report({'INFO'}, "Select 2 objects  with physics 2D enabled")
            return {'CANCELLED'}
        
        self.body_a = ob_with_bodies[0]
        self.body_b = ob_with_bodies[1]
        
        scene_prismatic_joint = self.add_joint(context, event)
        scene_prismatic_joint.body_a = self.body_a
        scene_prismatic_joint.body_b = self.body_b


        return {'FINISHED'}
    

    def execute(self, context):



        return {'FINISHED'}