# from .props import register_props, unregister_props
# # from .operator import register_operators, unregister_operators
# from .panel import register_panels, unregister_panels
# from .gizmos import register_gizmos, unregister_gizmos
# from .operator import register_operators, unregister_operators

from .physics_2d import register_physics, unregister_physics

bl_info = {
    "name" : "Three plugin",
    "description" : "Three custom tools integration",
    "author" : "Gilles Boisson",
    "version" : (0,1),
    "blender": (2,90,0),
    "location" : "View3D",
    "category" : "3D view",
}

def register():
    register_physics()

def unregister():
    unregister_physics()

if __name__ == "__main__":
    register()