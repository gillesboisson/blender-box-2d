from math import pi
import typing
from bpy.props import *
import bpy
from mathutils import Matrix
from .physics_2d_prismatic_anchor_move_widget import Physics2DPrismaticAnchorMoveWidget
from .physics_2d_revolute_anchor_widget import Physics2DRevoluteAnchorMoveWidget
from .physics_2d_prismatic_axe_widget import Physics2DPrismaticAxeWidget
from .physics_2d_axe_rotation_widget import Physics2DAxeRotationWidget
from .physics_2d_distance_anchor_widget import Physics2DDistanceAnchorMoveWidget
from .physics_2d_distance_widget import Physics2DDistanceWidget
from .physics_2d_wheel_anchor_base_widget import Physics2DWheelAnchorBaseMoveWidget
from .physics_2d_axe_widget import Physics2DAxeWidget
from .physics_2d_rope_arc_widget import Physics2DRopeArcWidget
from .physics_2d_axe_limit_widget import Physics2DAxeLimitWidget
    
classes = (
    Physics2DRevoluteAnchorMoveWidget,
    Physics2DPrismaticAnchorMoveWidget,
    Physics2DPrismaticAxeWidget,
    Physics2DAxeRotationWidget,
    Physics2DDistanceAnchorMoveWidget,
    Physics2DDistanceWidget,
    Physics2DWheelAnchorBaseMoveWidget,
    Physics2DAxeWidget,
    Physics2DRopeArcWidget,
    Physics2DAxeLimitWidget
)

def register_physic_2d_joint_widgets():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister_physic_2d_joint_widgets():
    for cls in classes:
        bpy.utils.unregister_class(cls)





