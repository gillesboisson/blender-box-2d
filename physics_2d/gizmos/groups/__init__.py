

from .body import register_body_groups, unregister_body_groups
from .joints import register_joints_groups, unregister_joints_groups

def register_groups():
    register_body_groups()
    register_joints_groups()

def unregister_groups():
    unregister_body_groups()
    unregister_joints_groups()
    