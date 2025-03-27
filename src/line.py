from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt
from graphic_object import GraphicObject
from point import Point
from utils import LINE_THICKNESS


class Line(GraphicObject):
    def __init__(self, name, point1: Point, point2: Point):
        super().__init__(name)
        self.point1 = point1
        self.point2 = point2

    def draw(self, painter, viewport, window):
        painter.setPen(QPen(Qt.GlobalColor.red, LINE_THICKNESS))

        # Transforma os pontos para a viewport
        transformed_p1 = (viewport.transform(self.point1, window))
        transformed_p2 = (viewport.transform(self.point2, window))
        
        painter.drawLine(int(transformed_p1.x), int(transformed_p1.y), int(transformed_p2.x), int(transformed_p2.y))
    def geometric_center(self):
        x_center = (self.point1.x + self.point2.x) / 2
        y_center = (self.point1.y + self.point2.y) / 2
        return x_center, y_center