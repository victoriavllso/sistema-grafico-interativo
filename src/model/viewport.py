from src.model.graphic_objects.point import Point
from src.model.window import Window
from src.utils.utils import VP_X_MAX, VP_X_MIN, VP_Y_MAX, VP_Y_MIN

class Viewport:
    def __init__(self, x_min = VP_X_MIN, x_max = VP_X_MAX, y_min = VP_Y_MIN, y_max = VP_Y_MAX):
        self.x_min = x_min        
        self.x_max = x_max
        self.y_min = y_min        
        self.y_max = y_max
    
    def transform(self, point:Point, window:Window) -> Point:
        """Aplica a transformação de viewport ao ponto dado."""
        x = ((point.scn_x - -1)/(1- -1)) * (VP_X_MAX)
        y = (1 - (point.scn_y - -1)/(1- -1)) * (VP_Y_MAX)
        name = point.name
        if name != "default":
            return Point(window=window,x = x, y= y,name= name)
        return Point(window = window, x = x,y =  y)
