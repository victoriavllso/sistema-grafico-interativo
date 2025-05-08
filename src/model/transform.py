import numpy as np
from src.model.graphic_objects.graphic_object import GraphicObject
from src.model.window import Window

class Transform:

    #---------- Matrizes de transformação ----------#

    @staticmethod
    def matrix_translate(tx:int, ty:int, tz:int) -> np.ndarray:
        """Matriz de translação"""
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [tx, ty, tz, 1]
        ])

    @staticmethod
    def matrix_scale(sx:int, sy:int, sz:int) -> np.ndarray:
        """Matriz de escala"""
        return np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def matrix_rotate_x(angle:int) -> np.ndarray:
        """Matriz de rotação"""
        angle = np.radians(angle)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        return np.array([
            [1, 0, 0, 0],
            [0, cos_a, -sin_a, 0],
            [0, sin_a, cos_a, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def matrix_rotate_y(angle:int) -> np.ndarray:
        """Matriz de rotação"""
        angle = np.radians(angle)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        return np.array([
            [cos_a, 0, sin_a, 0],
            [0, 1, 0, 0],
            [-sin_a, 0, cos_a, 0],
            [0, 0, 0, 1]
        ])
    
    @staticmethod
    def matrix_rotate_z(angle:int) -> np.ndarray:
        """Matriz de rotação"""
        angle = np.radians(angle)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        return np.array([
            [cos_a, -sin_a, 0, 0],
            [sin_a, cos_a, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
    
    #---------- Transformações de objetos gráficos ----------#

    @staticmethod
    def translate_object(obj:GraphicObject, dx:int, dy:int, dz:int) -> None:
        """Translada um objeto gráfico"""
        obj.receive_transform(Transform.matrix_translate(dx, dy, dz))

    @staticmethod
    def scale_object(obj:GraphicObject, sx:int, sy:int, sz:int) -> None:
        """Escala um objeto gráfico em torno do seu centro geométrico"""
        cx, cy, cz = obj.geometric_center()
        matrixs = [
            Transform.matrix_translate(-cx, -cy, -cz),
            Transform.matrix_scale(sx, sy, sz),
            Transform.matrix_translate(cx, cy, cz)
        ]
        for matrix in matrixs:
            obj.receive_transform(matrix)

    @staticmethod
    def rotate_object(obj: GraphicObject, angle: int, axis: str = 'z', px: int = 0, py: int = 0, pz: int = 0) -> None:
        """Rotaciona um objeto gráfico em torno de um ponto no eixo especificado (x, y ou z)"""
        if axis == 'x':
            rotation_matrix = Transform.matrix_rotate_x(angle)
        elif axis == 'y':
            rotation_matrix = Transform.matrix_rotate_y(angle)
        elif axis == 'z':
            rotation_matrix = Transform.matrix_rotate_z(angle)
        else:
            raise ValueError("Eixo de rotação inválido. Use 'x', 'y' ou 'z'.")

        matrixs = [
            Transform.matrix_translate(-px, -py, -pz),
            rotation_matrix,
            Transform.matrix_translate(px, py, pz)
        ]
        for matrix in matrixs:
            obj.receive_transform(matrix)

    @staticmethod
    def rotate_point_origin(x, y, z, angle, axis='z') -> tuple:
        """Rotaciona um ponto em torno da origem em torno do eixo especificado"""
        if axis == 'x':
            matrix_rotate = Transform.matrix_rotate_x(angle)
        elif axis == 'y':
            matrix_rotate = Transform.matrix_rotate_y(angle)
        elif axis == 'z':
            matrix_rotate = Transform.matrix_rotate_z(angle)
        else:
            raise ValueError("Eixo de rotação inválido. Use 'x', 'y' ou 'z'.")

        point = np.array([x, y, z, 1])  # coordenadas homogêneas
        result = np.dot(point, matrix_rotate)
        return result[0], result[1], result[2]

    #---------- Cálculo de ângulo entre vetores ----------#
    
    @staticmethod
    def calculate_angle(vector1, vector2) -> float:
        """Calcula o ângulo entre dois vetores (2D ou 3D)"""
        v1 = np.array(vector1)
        v2 = np.array(vector2)

        if v1.shape != v2.shape:
            raise ValueError(f"Vetores devem ter o mesmo número de dimensões. Recebido {v1.shape} e {v2.shape}.")

        v1 = v1 / np.linalg.norm(v1)
        v2 = v2 / np.linalg.norm(v2)
        result = np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))
        return result

    #---------- Conversão entre coordenadas de janela e coordenadas de tela ----------#

    @staticmethod
    def to_screen_coordinates(x, y, z, window) -> tuple:
        """Converte coordenadas de janela para coordenadas de tela"""
        center_x, center_y, center_z = window.get_center()
        x_min, y_min, z_min = window.get_min()
        x_max, y_max, z_max = window.get_max()
        scn_x = -1 + 2 * (x - (x_min - center_x)) / (
            (x_max - center_x) - (x_min - center_x)
        )
        scn_y = -1 + 2 * (y - (y_min - center_y)) / (
            (y_max - center_y) - (y_min - center_y)
        )
        scn_z = (z - z_min) / (z_max - z_min) if z_max != z_min else 0
        return scn_x, scn_y, scn_z
    
    @staticmethod
    def from_screen_coordinates(scn_x: float, scn_y: float, scn_z:float, window: Window) -> tuple[float, float]:
        """Converte coordenadas da tela para coordenadas da janela"""
        x = (scn_x + 1) / 2 * (window.x_max - window.x_min) + window.x_min
        y = (scn_y + 1) / 2 * (window.y_max - window.y_min) + window.y_min
        if hasattr(window, 'z_min') and hasattr(window, 'z_max'):
            z = scn_z * (window.z_max - window.z_min) + window.z_min
        else:
            z = scn_z
        return x, y, z
