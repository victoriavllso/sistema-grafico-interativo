from graphic_object import GraphicObject
from point import Point

class Wireframe(GraphicObject):
    def __init__(self, points: list[Point], color: tuple[int, int, int] = (0,0,0)):
        self.points = points
        self.color = color

    def draw(self):
        pass