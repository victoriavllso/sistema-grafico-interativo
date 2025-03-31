from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt
from src.model.graphic_object import GraphicObject
from src.model.point import Point
from src.model.utils import LINE_THICKNESS
import numpy as np


class Line(GraphicObject):
    def __init__(self, name, point1: Point, point2: Point):
        super().__init__(name)
        self.point1 = point1
        self.point2 = point2

    def draw(self, painter, viewport, window):
        painter.setPen(QPen(Qt.GlobalColor.red, LINE_THICKNESS))
        transformed_p1 = (viewport.transform(self.point1, window))
        transformed_p2 = (viewport.transform(self.point2, window))
        painter.drawLine(int(transformed_p1.x), int(transformed_p1.y), int(transformed_p2.x), int(transformed_p2.y))

    def geometric_center(self):
        x_center = (self.point1.x + self.point2.x) / 2
        y_center = (self.point1.y + self.point2.y) / 2
        return x_center, y_center

    def receive_transform(self, matrix) -> None:
        point1_matrix = np.array([self.point1.x, self.point1.y, 1])
        new_point1 = point1_matrix @ matrix
        self.point1.x = new_point1[0]
        self.point1.y = new_point1[1]

        point2_matrix = np.array([self.point2.x, self.point2.y, 1])
        new_point2 = point2_matrix @ matrix
        self.point2.x = new_point2[0]
        self.point2.y = new_point2[1]