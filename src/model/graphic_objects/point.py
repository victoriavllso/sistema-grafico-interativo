from src.model.graphic_objects.graphic_object import GraphicObject
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt
from src.utils.utils import POINT_THICKNESS
import numpy as np
from src.model.transform import Transform
from src.model.projection import Projection

class Point(GraphicObject):
    def __init__(self, window, x: int, y: int, z:int, name="default", color=Qt.GlobalColor.green):
        super().__init__(name=name, color=color, window=window)
        self._x = x
        self._y = y
        self._z = z
        self.scn_x = 0
        self.scn_y = 0
        self.scn_z = 0
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
    

    @property
    def z(self):
        return self._z
    
    @z.setter
    def z(self, value: float):
        self._z = value
        self.convert_coordinates()

    def draw(self, painter, viewport):
        if not self.inside_window:
            return
        
        vrp = self.window.get_vrp()
        vpn = self.window.get_vpn()

        # aplica a projeção ortogonal
        projected_points = Projection.orthogonal_projection(
            [(self.x, self.y, self.z, 1)], # coord homogeneas
            vrp, vpn, self.window
        )

        print(f'projected_points: {projected_points}')

        x, y = projected_points[0]

        transformed_point = viewport.transform(self, self.window)
        
        x, y = int(transformed_point.x), int(transformed_point.y)
        painter.setPen(QPen(self.color, POINT_THICKNESS))

        painter.drawPoint(x, y)

    def geometric_center(self):
        return self.x, self.y, self.z

    def receive_transform(self, matrix) -> None:
        point_matrix = np.array([self.x, self.y,self.z, 1])
        new_point = point_matrix @ matrix
        self.x = new_point[0]
        self.y = new_point[1]
        self.z = new_point[2]
    
    def __str__(self):
        color_name = self.color.name() if callable(getattr(self.color, "name", None)) else self.color
        return f"Point({self.name}, {self.x}, {self.y}, {self.x} color={color_name})"

    def convert_coordinates(self) -> None:
        """Converte as coordenadas do ponto do espaço da janela para o espaço da cena"""

        center_x, center_y,center_z = self.window.get_center()

        # Translação para centralizar no (0, 0)
        translated = np.dot([self.x, self.y, self.z, 1], Transform.matrix_translate(-center_x, -center_y, -center_z))
        x, y, z = translated[0], translated[1], translated[2]

        # Rotaciona conforme a direção da janela
        angle = Transform.calculate_angle((0, 1), self.window.direction) * (180 / np.pi)
        if self.window.direction[0] < 0:
            angle = 360 - angle
        if angle != 0:
            x, y, z = Transform.rotate_point_origin(x, y, z, angle)

        # Converte para coordenadas da cena
        self.scn_x, self.scn_y, self.scn_z = Transform.to_screen_coordinates(x, y,z, self.window)

    def from_scene_coordinates(self, scn_x: float, scn_y: float, scn_z:float) -> None:
        """Converte coordenadas da cena para coordenadas da janela"""

        # Inverte a conversão para coordenadas da cena
        x, y, z = Transform.from_screen_coordinates(scn_x, scn_y,scn_z, self.window)

        # Inverte a rotação
        angle = Transform.calculate_angle((0, 1), self.window.direction) * (180 / np.pi)
        if self.window.direction[0] < 0:
            angle = 360 - angle
        if angle != 0:
            x, y, z = Transform.rotate_point_origin(x, y,z, -angle)

        # Inverte a translação
        center_x, center_y, center_z = self.window.get_center()
        translated = np.dot([x, y,z, 1], Transform.matrix_translate(center_x, center_y, center_z))

        # Define os valores reais
        self.x, self.y, self.z = translated[0], translated[1], translated[2]
        self.scn_x, self.scn_y, self._z = scn_x, scn_y, scn_z


    def get_points_obj(self):
        return f'v {self.x} {self.y} {self.z} 0\n'
    
    def get_type_obj(self):
        return 'p'
