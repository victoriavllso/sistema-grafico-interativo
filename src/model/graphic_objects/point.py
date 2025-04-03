from src.model.graphic_objects.graphic_object import GraphicObject
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt
from src.utils.utils import POINT_THICKNESS
import numpy as np


class Point(GraphicObject):
    def __init__(self, x: int, y: int, name="default", color=Qt.GlobalColor.green):
        super().__init__(name, color)
        self.x = x
        self.y = y

    def draw(self, painter, viewport, window):
        transformed_point = viewport.transform(self, window)
        x, y = int(transformed_point.x), int(transformed_point.y)
        painter.setPen(QPen(self.color, POINT_THICKNESS))
        painter.drawPoint(x, y)

    def geometric_center(self):
        return self.x, self.y

    def receive_transform(self, matrix) -> None:
        point_matrix = np.array([self.x, self.y, 1])
        new_point = point_matrix @ matrix
        self.x = new_point[0]
        self.y = new_point[1]
    
    def __str__(self):
        return f"Point({self.name}, {self.x}, {self.y}, color={self.color.name()})"