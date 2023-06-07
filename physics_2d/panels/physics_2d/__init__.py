
from .physics_2d_body_panel import ThreePhysics2DBodyPanel
from .physics_2d_body_settings_panel import ThreePhysics2DBodySettingsPanel
from .physics_2d_body_shape_panel import ThreePhysics2DBodyShapePanel
from .physics_2d_scene_settings_panel import ThreePhysics2DSceneSettingsPanel
        

classes = (
    ThreePhysics2DBodyPanel,
    ThreePhysics2DBodySettingsPanel,
    ThreePhysics2DBodyShapePanel,
)

from bpy.utils import register_class, unregister_class

def register_physics_2d_panels() -> None:
    for panelClass in classes:
        register_class(panelClass)


def unregister_physics_2d_panels() -> None:
    revertClasses = reversed(classes)
    for panelClass in revertClasses:
        unregister_class(panelClass)

