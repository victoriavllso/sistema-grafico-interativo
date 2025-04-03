import numpy as np
from src.model.graphic_objects.point import Point

class Transform:
    @staticmethod
    def matrix_translate(dx, dy):
        """Matriz de translação"""
        return np.array([[1, 0, 0],
                         [0, 1, 0],
                         [dx, dy, 1]])

    @staticmethod
    def matrix_scale(sx, sy):
        """Matriz de escala"""
        return np.array([[sx, 0, 0],
                         [0, sy, 0],
                         [0, 0, 1]])

    @staticmethod
    def matrix_rotate(angle):
        """Matriz de rotação"""
        angle = np.radians(angle)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        return np.array([[cos_a, -sin_a, 0],
                         [sin_a, cos_a, 0],
                         [0, 0, 1]])

    @staticmethod
    def translate_object(obj, dx, dy):
        """Translada um objeto gráfico"""
        obj.receive_transform(Transform.matrix_translate(dx, dy))

    @staticmethod
    def scale_object(obj, sx, sy):
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
    def rotate_object(obj, angle, px=0, py=0):
        """Rotaciona um objeto gráfico em torno de um ponto"""
        matrixs = [
            Transform.matrix_translate(-px, -py),
            Transform.matrix_rotate(angle),
            Transform.matrix_translate(px, py)
        ]
        for matrix in matrixs:
            obj.receive_transform(matrix)