# from bpy.utils import register_class, unregister_class

# from .physics_3d.physics_3D_body_panel import ThreePhysics3DBodyPanel
# from .physics_2d import register_physics_2d_panels, unregister_physics_2d_panels
# from .scene_physics_settings_panel import register_physics_scene_panels, unregister_physics_scene_panels

# from .entity_panel import ThreeEntityPanel

# panelClasses = (ThreeEntityPanel, ThreePhysics3DBodyPanel )

# def register_panels() -> None:
#     for panelClass in panelClasses:
#         register_class(panelClass)
#     register_physics_2d_panels()
#     register_physics_scene_panels()

# def unregister_panels() -> None:
#     for panelClass in panelClasses:
#         unregister_class(panelClass)
#     unregister_physics_2d_panels()
#     unregister_physics_scene_panels()

from .physics_2d import register_physics_2d_panels, unregister_physics_2d_panels
from .physics_3d import register_physics_3d_panels, unregister_physics_3d_panels

def register_panels() -> None:
    register_physics_2d_panels()
    # register_physics_3d_panels()

def unregister_panels() -> None:
    unregister_physics_2d_panels()
    # unregister_physics_3d_panels()

