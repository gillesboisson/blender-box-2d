
from .physics_2d_body_panel import ThreePhysics2DBodyPanel
from .physics_2d_body_settings_panel import ThreePhysics2DBodySettingsPanel
from .physics_2d_body_shape_panel import ThreePhysics2DBodyShapePanel
from .physics_2d_scene_settings_panel import ThreePhysics2DSceneSettingsPanel
from .physics_2d_revolute_joint_panel import ThreePhysics2DSceneRevoluteJointPanel, ThreePhysics2DObjectRevoluteJointPanel
from .physics_2d_prismatic_joint_panel import ThreePhysics2DScenePrismaticJointPanel, ThreePhysics2DObjectPrismaticJointPanel
from .physics_2d_distance_joint_panel import ThreePhysics2DSceneDistanceJointPanel, ThreePhysics2DObjectDistanceJointPanel
from .physics_2d_wheel_joint_panel import ThreePhysics2DSceneWheelJointPanel, ThreePhysics2DObjectWheelJointPanel
from .physics_2d_rope_joint_panel import ThreePhysics2DSceneRopeJointPanel, ThreePhysics2DObjectRopeJointPanel
from .physics_2d_viewport_settings import ThreePhysics2DViewportSettingsPanel
        

classes = (
    ThreePhysics2DBodyPanel,
    ThreePhysics2DBodySettingsPanel,
    ThreePhysics2DBodyShapePanel,
    ThreePhysics2DSceneSettingsPanel,
    ThreePhysics2DSceneRevoluteJointPanel,
    ThreePhysics2DViewportSettingsPanel,
    ThreePhysics2DObjectRevoluteJointPanel,
    ThreePhysics2DScenePrismaticJointPanel,
    ThreePhysics2DObjectPrismaticJointPanel,
    ThreePhysics2DSceneDistanceJointPanel,
    ThreePhysics2DObjectDistanceJointPanel,
    ThreePhysics2DSceneWheelJointPanel,
    ThreePhysics2DObjectWheelJointPanel,
    ThreePhysics2DSceneRopeJointPanel,
    ThreePhysics2DObjectRopeJointPanel,
)

from bpy.utils import register_class, unregister_class

def register_panels() -> None:
    for panelClass in classes:
        register_class(panelClass)


def unregister_panels() -> None:
    revertClasses = reversed(classes)
    for panelClass in revertClasses:
        unregister_class(panelClass)

