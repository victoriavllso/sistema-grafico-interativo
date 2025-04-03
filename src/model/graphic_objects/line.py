from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt
from src.model.graphic_objects.graphic_object import GraphicObject
from src.model.graphic_objects.point import Point
from src.utils.utils import LINE_THICKNESS
import numpy as np


class Line(GraphicObject):
    def __init__(self, name, point1: Point, point2: Point, color=Qt.GlobalColor.red):
        super().__init__(name, color)
        self.points = [point1, point2]

    def draw(self, painter, viewport, window):
        """Desenha a linha no viewport."""
        painter.setPen(QPen(self.color, LINE_THICKNESS))
        transformed_p1 = viewport.transform(self.points[0], window)
        transformed_p2 = viewport.transform(self.points[1], window)
        painter.drawLine(int(transformed_p1.x), int(transformed_p1.y), int(transformed_p2.x), int(transformed_p2.y))

    def geometric_center(self) -> tuple[float, float]:
        """Retorna o ponto médio da linha como uma tupla (x, y)."""
        return (
            (self.points[0].x + self.points[1].x) / 2,
            (self.points[0].y + self.points[1].y) / 2
        )

    def receive_transform(self, matrix) -> None:
        point1_matrix = np.array([self.points[0][0], self.points[0][1], 1])
        new_point1 = point1_matrix @ matrix
        self.points[0][0] = new_point1[0]
        self.points[0][1] = new_point1[1]

        point2_matrix = np.array([self.points[1][0], self.points[1][1], 1])
        new_point2 = point2_matrix @ matrix
        self.points[1][0] = new_point2[0]
        self.points[1][1] = new_point2[1]

    def __str__(self):
        return f"Line({self.name}, {self.points[0]}, {self.points[1]}, color={self.color.name()})"
