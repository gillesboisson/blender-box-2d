from .physics_2d_create_revolute_joint import Physics2DCreateRevoluteJointOperator
from .physics_2d_create_prismatic_joint import Physics2DCreatePrismaticJointOperator
from .physics_2d_create_distance_joint import Physics2DCreateDistanceJointOperator
from .physics_2d_create_wheel_joint import Physics2DCreateWheelJointOperator
from .physics_2d_create_rope_joint import Physics2DCreateRopeJointOperator
from .physics_2d_delete_revolute_joint import Physics2DDeleteRevoluteJointOperator
from .physics_2d_delete_prismatic_joint import Physics2DDeletePrismaticJointOperator
from .physics_2d_delete_distance_joint import Physics2DDeleteDistanceJointOperator
from .physics_2d_delete_wheel_joint import Physics2DDeleteWheelJointOperator
from .physics_2d_delete_rope_joint import Physics2DDeleteRopeJointOperator

classes = (
    Physics2DCreateRevoluteJointOperator,
    Physics2DDeleteRevoluteJointOperator,
    Physics2DCreatePrismaticJointOperator,
    Physics2DDeletePrismaticJointOperator,
    Physics2DCreateDistanceJointOperator,
    Physics2DDeleteDistanceJointOperator,
    Physics2DCreateWheelJointOperator,
    Physics2DDeleteWheelJointOperator,
    Physics2DCreateRopeJointOperator,
    Physics2DDeleteRopeJointOperator

)

from bpy.utils import register_class, unregister_class

def register_joints_operators() -> None:
    for panelClass in classes:
        register_class(panelClass)


def unregister_joints_operators() -> None:
    revertClasses = reversed(classes)
    for panelClass in revertClasses:
        unregister_class(panelClass)

