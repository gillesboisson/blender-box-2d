
from .widgets import register_widgets, unregister_widgets
from .groups import register_groups, unregister_groups


def register_gizmos() -> None:
    register_widgets()
    register_groups()

def unregister_gizmos() -> None:
    unregister_widgets()
    unregister_groups()
