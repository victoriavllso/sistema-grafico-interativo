from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt
from src.model.graphic_objects.graphic_object import GraphicObject
from src.model.graphic_objects.point import Point
from src.utils.utils import LINE_THICKNESS
import numpy as np


class Line(GraphicObject):
    def __init__(self,window, name, point1: Point, point2: Point, color=Qt.GlobalColor.red):
        super().__init__(name, color)
        self.points = [point1, point2]
        self.window = window

    def x1(self):
        return self.points[0].x
    
    def y1(self):
        return self.points[0].y
    
    def x2(self):
        return self.points[1].x
    
    def y2(self):
        return self.points[1].y


    def draw(self, painter, viewport):
        """Desenha a linha no viewport."""
        painter.setPen(QPen(self.color, LINE_THICKNESS))

        for points in self.points:
            points.convert_coordinates()

        transformed_p1 = viewport.transform(self.points[0], self.window)
        transformed_p2 = viewport.transform(self.points[1], self.window)
        print(f'reta desenhada nos pontos: {transformed_p1.x}, {transformed_p1.y} -> {transformed_p2.x}, {transformed_p2.y}')
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

    def get_points_obj(self):
        return f'v {self.points[0].x}, {self.points[0].y} \nv {self.points[1].x}, {self.points[1].y} \n'
    
    def get_type_obj(self):
        return 'l'