from point import Point
from window import Window
from utils import WIDTH, HEIGHT

class Viewport:
    def __init__(self, width = WIDTH, height = HEIGHT):
        self.width = width
        self.height = height
    
    def transform(self, point: Point, window: Window) -> Point:
        x = (point.x - window.x_min) / (window.x_max - window.x_min) * self.width
        y = (1 - (point.y - window.y_min)) / (window.y_max - window.y_min) * self.height
        return Point(x, y)

    # ---------- DONE ---------- #