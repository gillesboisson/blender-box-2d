from bpy.utils import register_class, unregister_class


from .box_widget import BoxWidget
from .sphere_widget import SphereWidget
from .square_line_widget import SquareLineWidget
from .square_fill_widget import SquareFillWidget
from .circle_widget import CircleWidget
from .cylinder_widget import CylinderWidget
from .polygon_widget import PolygonWidget



widgetsClasses = (
    BoxWidget,
    SquareLineWidget,
    SphereWidget,
    CircleWidget,
    CylinderWidget,
    PolygonWidget,
    SquareFillWidget
)

def register_widgets() -> None:
    for operatorClass in widgetsClasses:
        register_class(operatorClass)

def unregister_widgets() -> None:
    for operatorClass in widgetsClasses:
        unregister_class(operatorClass)
