import numpy as np
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
    def convert_scn_coords(scn_x: float, scn_y: float, window: Window) -> tuple[float, float]:
        """Converte coordenadas da cena para coordenadas da janela"""
        x = (scn_x + 1) / 2 * (window.x_max - window.x_min) + window.x_min
        y = (scn_y + 1) / 2 * (window.y_max - window.y_min) + window.y_min
        return x, y
    
    @staticmethod
    def calculate_angle(vector1, vector2) -> float:
        """Calcula o ângulo entre dois vetores"""
        v1 = vector1 / np.linalg.norm(vector1)
        v2 = vector2 / np.linalg.norm(vector2)
        result = np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))
        return result
    
    @staticmethod
    def rotate_point_origin(x, y, angle) -> tuple:
        """Rotaciona um ponto em torno da origem"""
        matrix_rotate = Transform.matrix_rotate(angle)
        matrix_homogenous = np.array([x, y, 1])
        result = np.dot(matrix_homogenous, matrix_rotate)
        x = result[0]
        y = result[1]
        return x, y

    @staticmethod
    def to_screen_coordinates(x, y, window) -> tuple:
        """Converte coordenadas de janela para coordenadas de tela"""
        center_x, center_y = window.get_center()
        x_min, y_min = window.get_min()
        x_max, y_max = window.get_max()
        scn_x = -1 + 2 * (x - (x_min - center_x)) / (
            (x_max - center_x) - (x_min - center_x)
        )
        scn_y = -1 + 2 * (y - (y_min - center_y)) / (
            (y_max - center_y) - (y_min - center_y)
        )
        return scn_x, scn_y
