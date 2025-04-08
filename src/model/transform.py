import numpy as np
from src.model.graphic_objects.point import Point
from src.model.graphic_objects.graphic_object import GraphicObject
from src.model.window import Window

class Transform:
    @staticmethod
    def matrix_translate(dx:int, dy:int) -> np.ndarray:
        """Matriz de translação"""
        return np.array([[1, 0, 0],
                         [0, 1, 0],
                         [dx, dy, 1]])

    @staticmethod
    def matrix_scale(sx:int, sy:int) -> np.ndarray:
        """Matriz de escala"""
        return np.array([[sx, 0, 0],
                         [0, sy, 0],
                         [0, 0, 1]])

    @staticmethod
    def matrix_rotate(angle:int) -> np.ndarray:
        """Matriz de rotação"""
        angle = np.radians(angle)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        return np.array([[cos_a, -sin_a, 0],
                         [sin_a, cos_a, 0],
                         [0, 0, 1]])

    @staticmethod
    def translate_object(obj:GraphicObject, dx:int, dy:int) -> None:
        """Translada um objeto gráfico"""
        obj.receive_transform(Transform.matrix_translate(dx, dy))

    @staticmethod
    def scale_object(obj:GraphicObject, sx:int, sy:int) -> None:
        """Escala um objeto gráfico em torno do seu centro geométrico"""
        cx, cy = obj.geometric_center()
        matrixs = [
            Transform.matrix_translate(-cx, -cy),
            Transform.matrix_scale(sx, sy),
            Transform.matrix_translate(cx, cy)
        ]
        for matrix in matrixs:
            obj.receive_transform(matrix)

    @staticmethod
    def rotate_object(obj:GraphicObject, angle:int, px:int=0, py:int=0) -> None:
        """Rotaciona um objeto gráfico em torno de um ponto"""
        matrixs = [
            Transform.matrix_translate(-px, -py),
            Transform.matrix_rotate(angle),
            Transform.matrix_translate(px, py)
        ]
        for matrix in matrixs:
            obj.receive_transform(matrix)

    @staticmethod
    def convert_scn(point:Point, window:Window) -> Point:
        """Converte um ponto do espaço de cena para o espaço da janela"""
        x = (point.scn_x - -1) / (1 - -1) * (window.x_max)
        y =  (point.scn_y - -1) / (1 - -1) * (window.y_max)
        name = point.name
        if name != "default":
            return Point(x, y, name)
        return Point(x, y)
