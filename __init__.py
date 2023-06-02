from .props import register_props, unregister_props
# from .operator import register_operators, unregister_operators
from .panel import register_panels, unregister_panels
from .gizmos import register_gizmos, unregister_gizmos
from .operator import register_operators, unregister_operators


bl_info = {
    "name" : "Test plugin",
    "description" : "Plugin test",
    "author" : "Gilles Boisson",
    "version" : (0,1),
    "blender": (2,90,0),
    "location" : "View3D",
    "category" : "3D view",
}

def register():
    register_props()
    # register_operators()
    register_panels()
    register_gizmos()
    register_operators()

def unregister():
    unregister_props()
    # unregister_operators()
    unregister_panels()
    unregister_gizmos()
    unregister_operators()