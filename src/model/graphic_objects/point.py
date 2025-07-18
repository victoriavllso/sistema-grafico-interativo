from src.model.graphic_objects.graphic_object import GraphicObject
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt
from src.utils.utils import POINT_THICKNESS
import numpy as np
from src.model.transform import Transform

class Point(GraphicObject):
    def __init__(self, window, x: int, y: int, name="default", color=Qt.GlobalColor.green):
        super().__init__(name=name, color=color, window=window)
        self._x = x
        self._y = y
        self.scn_x = 0
        self.scn_y = 0
        self.inside_window = False
        self.convert_coordinates()

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value
        self.convert_coordinates()

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value
        self.convert_coordinates()

    def draw(self, painter, viewport):
        if not self.inside_window:
            return
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
        color_name = self.color.name() if callable(getattr(self.color, "name", None)) else self.color
        return f"Point({self.name}, {self.x}, {self.y}, color={color_name})"

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

    def from_scene_coordinates(self, scn_x: float, scn_y: float) -> None:
        """Converte coordenadas da cena para coordenadas da janela"""

        # Inverte a conversão para coordenadas da cena
        x, y = Transform.from_screen_coordinates(scn_x, scn_y, self.window)

        # Inverte a rotação
        angle = Transform.calculate_angle((0, 1), self.window.direction) * (180 / np.pi)
        if self.window.direction[0] < 0:
            angle = 360 - angle
        if angle != 0:
            x, y = Transform.rotate_point_origin(x, y, -angle)

        # Inverte a translação
        center_x, center_y = self.window.get_center()
        translated = np.dot([x, y, 1], Transform.matrix_translate(center_x, center_y))

        # Define os valores reais
        self.x, self.y = translated[0], translated[1]
        self.scn_x, self.scn_y = scn_x, scn_y


    def get_points_obj(self):
        return f'v {self.x} {self.y} 0\n'
    
    def get_type_obj(self):
        return 'p'
