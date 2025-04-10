from src.model.graphic_objects.graphic_object import GraphicObject
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt
from src.utils.utils import POINT_THICKNESS
import numpy as np
from src.model.transform import Transform


class Point(GraphicObject):
    def __init__(self, window, x: int, y: int, name="default", color=Qt.GlobalColor.green):
        super().__init__(name, color)
        self.x = x
        self.y = y
        self.scn_x = 0
        self.scn_y = 0
        self.window = window
        self.convert_coordinates()

    def draw(self, painter, viewport):
        self.convert_coordinates()
        transformed_point = viewport.transform(self, self.window)
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

    def convert_coordinates(self) -> None:
        """Converte as coordenadas do ponto do espaço da janela para o espaço da cena"""
        center_x, center_y = self.window.get_center()

        # Translação para centralizar no (0, 0)
        translated = np.dot([self.x, self.y, 1], Transform.matrix_translate(-center_x, -center_y))
        x, y = translated[0], translated[1]

        # Rotaciona conforme a direção da janela
        angle = Transform.calculate_angle((0, 1), self.window.direction) * (180 / np.pi)
        if self.window.direction[0] < 0:
            angle = 360 - angle
        if angle != 0:
            x, y = Transform.rotate_point_origin(x, y, angle)

        # Converte para coordenadas da cena
        self.scn_x, self.scn_y = Transform.to_screen_coordinates(x, y, self.window)

    def get_points_obj(self):
        return f'v {self.x} {self.y} 0\n'
    
    def get_type_obj(self):
        return 'p'
