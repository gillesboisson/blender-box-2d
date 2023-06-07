

import bpy
from .panels import register_panels, unregister_panels
from .props import register_props, unregister_props
from .gizmos import register_gizmos, unregister_gizmos



def register_physics():
    register_panels()
    register_props()
    register_gizmos()

def unregister_physics():
    unregister_panels()
    unregister_props()
    unregister_gizmos()
