
from .physics_2d_body_panel import ThreePhysics2DBodyPanel
from .physics_2d_body_settings_panel import ThreePhysics2DBodySettingsPanel
from .physics_2d_body_shape_panel import ThreePhysics2DBodyShapesPanel
from .physics_2d_scene_settings_panel import ThreePhysics2DSceneSettingsPanel

from .physics_2d_joint_panels import ThreePhysics2DSceneJointPanel, ThreePhysics2DObjectJointPanel
from .physics_2d_viewport_settings import ThreePhysics2DViewportSettingsPanel
from .physics_2d_tools_panel import ThreePhysics2DToolsPanel
        

classes = (
    ThreePhysics2DSceneSettingsPanel,
    ThreePhysics2DBodyPanel,
    ThreePhysics2DBodySettingsPanel,
    ThreePhysics2DBodyShapesPanel,
    ThreePhysics2DViewportSettingsPanel,
    ThreePhysics2DSceneJointPanel,
    ThreePhysics2DObjectJointPanel,
    ThreePhysics2DToolsPanel

)

from bpy.utils import register_class, unregister_class

def register_panels() -> None:
    for panelClass in classes:
        register_class(panelClass)


def unregister_panels() -> None:
    revertClasses = reversed(classes)
    for panelClass in revertClasses:
        unregister_class(panelClass)

