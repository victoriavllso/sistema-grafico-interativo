from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt
from src.model.graphic_objects.graphic_object import GraphicObject
from src.model.graphic_objects.point import Point
from src.utils.utils import LINE_THICKNESS
import numpy as np


class Line(GraphicObject):
    def __init__(self, window, name, point1: Point, point2: Point, color=Qt.GlobalColor.red):
        super().__init__(name, color, window)
        self.points = [point1, point2]

    def x1(self) -> float:
        """Retorna a coordenada x do primeiro ponto da linha."""
        return self.points[0].x
    
    def y1(self) -> float:
        """Retorna a coordenada y do primeiro ponto da linha."""
        return self.points[0].y
    
    def x2(self) -> float:
        """Retorna a coordenada x do segundo ponto da linha."""
        return self.points[1].x
    
    def y2(self) -> float:
        """Retorna a coordenada y do segundo ponto da linha."""
        return self.points[1].y

    def draw(self, painter, viewport):
        """Desenha a linha no viewport."""

        for point in self.points:
            if not point.inside_window:
                return

        painter.setPen(QPen(self.color, LINE_THICKNESS))

        transformed_p1 = viewport.transform(self.points[0], self.window)
        transformed_p2 = viewport.transform(self.points[1], self.window)

        painter.drawLine(int(transformed_p1.x), int(transformed_p1.y), int(transformed_p2.x), int(transformed_p2.y))

    def geometric_center(self) -> tuple[float, float]:
        """Retorna o ponto médio da linha como uma tupla (x, y)."""
        return (
            (self.points[0].x + self.points[1].x) / 2,
            (self.points[0].y + self.points[1].y) / 2
        )

    def receive_transform(self, matrix) -> None:
        """Aplica a transformação da matriz de transformação à linha."""
        point1_matrix = np.array([self.points[0].x, self.points[0].y, 1])
        new_point1 = point1_matrix @ matrix
        self.points[0].x = new_point1[0]
        self.points[0].y = new_point1[1]

        point2_matrix = np.array([self.points[1].x, self.points[1].y, 1])
        new_point2 = point2_matrix @ matrix
        self.points[1].x = new_point2[0]
        self.points[1].y = new_point2[1]

    def __str__(self):
        return f"Line({self.name}, {self.points[0]}, {self.points[1]}, color={self.color.name()})"

    def get_points_obj(self) -> str:
        return f'v {self.points[0].x}, {self.points[0].y} \nv {self.points[1].x}, {self.points[1].y} \n'
    
    def get_type_obj(self) -> str:
        return 'l'
