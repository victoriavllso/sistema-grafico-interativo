from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt
from graphic_object import GraphicObject
from point import Point


class Line(GraphicObject):
    def __init__(self, point1: Point, point2: Point):
        super().__init__()
        self.point1 = point1
        self.point2 = point2

    def draw(self, painter, viewport, window):
        # Transforma os pontos para a viewport
        transformed_p1 = (viewport.transform(self.point1, window))
        transformed_p2 = (viewport.transform(self.point2, window))
        
        painter.drawLine(int(transformed_p1.x), int(transformed_p1.y), int(transformed_p2.x), int(transformed_p2.y))
