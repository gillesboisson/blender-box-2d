

import bpy

from bpy.types import Context, Event

import bpy

from bpy.types import Context, Event

class Physics2DCreateJointOperator(bpy.types.Operator):

    def add_joint(self, context, event):
        return None
    
    def set_joint_props(self, context, joint, body_a, body_b):
        return

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
        
        joint = self.add_joint(context, event)
        joint.body_a = self.body_a
        joint.body_b = self.body_b

        self.set_joint_props(context, joint, self.body_a, self.body_b)

        return {'FINISHED'}
    

    def execute(self, context):



        return {'FINISHED'}