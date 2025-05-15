from src.model.graphic_objects.graphic_object import GraphicObject
from src.model.graphic_objects.wireframe import Wireframe

from PyQt6.QtCore import Qt

from typing import List
import numpy as np
from itertools import combinations

class Object(GraphicObject):
    def __init__(self, faces: Wireframe, name, color = Qt.GlobalColor.black, window=None):
        super().__init__(name, color, window)
        self.faces = [faces]

    def draw(self, painter, viewport) -> None:
        for face in self.faces:
            face.draw(painter, viewport)
            for p in getattr(face, "points", []):
                p.inside_window = False

    def add_face(self, face: Wireframe) -> None:
        """
        Adiciona uma face ao objeto 3D.
        """
        if isinstance(face, Wireframe):
            self.faces.append(face)
        else:
            raise TypeError("A face must be an instance of Wireframe.")

    def geometric_center(self) -> tuple[float, float]:
        x = 0
        y = 0
        for face in self.faces:
            x += face.geometric_center()[0]
            y += face.geometric_center()[1]
        x /= len(self.faces)
        y /= len(self.faces)
        return x, y

    def receive_transform(self, matrix) -> None:
        for face in self.faces:
            face.receive_transform(matrix)

    def __str__(self):
        pass

    def get_points_obj(self):
        points = []
        for face in self.faces:
            points.extend(face.get_points_obj())
        return points

    def get_type_obj(self):
        types = []
        for face in self.faces:
            types.extend(face.get_type_obj())
        return types
    
