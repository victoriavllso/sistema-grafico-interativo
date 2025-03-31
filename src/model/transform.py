import numpy as np
from src.model.point import Point
from src.model.line import Line
from src.model.wireframe import Wireframe

class Transform:
    def __init__(self):
        pass

    # homogeneous coordinates systems
    def matrix_translate(self, dx, dy):
        matrix_translate = np.array([[1, 0, 0],
                                     [0, 1, 0],
                                     [dx, dy, 1]])
        return matrix_translate
    
    def matrix_scale(self, sx, sy):
        matrix_scale = np.array([[sx, 0, 0],
                                 [0, sy, 0],
                                 [0, 0, 1]])
        return matrix_scale
    
    def matrix_rotate(self, angle):
        matrix_rotate = np.array([[np.cos(angle), -np.sin(angle), 0],
                                  [np.sin(angle), np.cos(angle), 0],
                                  [0, 0, 1]])
        return matrix_rotate
    
    # methods to transform objects
    def translate_object(self, object, dx, dy):
        object.receive_transform(self.matrix_translate(dx, dy))

    def scale_object(self, object, sx, sy):
        obj_center = object.geometric_center()
        cx, cy = obj_center[0], obj_center[1]
        matrixs = [self.matrix_translate(-cx,-cy),  self.matrix_scale(sx, sy), self.matrix_translate(cx, cy)]
        for matrix in matrixs:
            object.receive_transform(matrix)

    def rotate_object(self, object, angle, use_center: bool, px=0, py=0):
        obj_center = object.geometric_center()
        cx, cy = obj_center[0], obj_center[1]
        if use_center:  # rotação no ponto 0 ou arbitrário
            matrixs = [self.matrix_translate(-px,-py), self.matrix_rotate(angle), self.matrix_translate(px, py)]
            for matrix in matrixs:
                object.receive_transform(matrix)
        else:
            matrixs = [self.matrix_translate(-cx,-cy), self.matrix_rotate(angle), self.matrix_translate(cx, cy)]
            for matrix in matrixs:
                object.receive_transform(matrix)
