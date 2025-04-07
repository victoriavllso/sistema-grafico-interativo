from src.model.graphic_objects.graphic_object import GraphicObject
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt
from src.utils.utils import POINT_THICKNESS
import numpy as np


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
        print(f"DRAWING POINT AT: ({x}, {y})")

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
    
    def convert_coordinates(self):
        translation = (-self.window.get_center()[0], -self.window.get_center()[1])

        matrix_homogenous = [self.x, self.y, 1]
        matrix_translate = [
            [1, 0, 0],
            [0, 1, 0],
            [translation[0], translation[1], 1]
        ]
        result = np.dot(matrix_homogenous, matrix_translate)
        x = result[0]
        y = result[1]
        angle = self.calculate_angle((0,1),self.window.direction)/(np.pi/180)
        if angle != 0:
            if self.window.direction[0] < 0:
                angle = 360 - angle
            x, y = self.rotate_point_origin(x, y, angle)
        self.scn_x = -1 + 2 * (x - (self.window.x_min -self.window.get_center()[0])) / ((self.window.x_max -self.window.get_center()[0]) - (self.window.x_min -self.window.get_center()[0]))
        self.scn_y = -1 + 2 * (y - (self.window.y_min -self.window.get_center()[1])) / ((self.window.y_max -self.window.get_center()[1]) - (self.window.y_min -self.window.get_center()[1]))

    def calculate_angle(self, vector1, vector2):
        v1 = vector1 / np.linalg.norm(vector1)
        v2 = vector2 / np.linalg.norm(vector2)
        result = np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))
        return result
    def rotate_point_origin(self,x, y, angle):
        angle *= (np.pi / 180)
        matrix_rotate = [
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ]
        matrix_homogenous= np.array([x, y, 1])
        result = np.dot(matrix_homogenous, matrix_rotate)
        x = result[0]
        y = result[1]
        return x, y
    
    def get_points_obj(self):
        return f'v {self.x} {self.y} 0\n'
    
    def get_type_obj(self):
        return 'p'