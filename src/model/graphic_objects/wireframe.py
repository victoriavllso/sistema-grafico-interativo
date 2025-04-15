from src.model.graphic_objects.graphic_object import GraphicObject
from src.model.graphic_objects.point import Point
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt
from src.utils.utils import LINE_THICKNESS
import numpy as np
from PyQt6.QtGui import QBrush
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPolygonF

class Wireframe(GraphicObject):
    def __init__(self,window, name, points: list[Point], color=Qt.GlobalColor.blue, filled=True):
        super().__init__(name, color)
        if not self._is_valid_polygon(points):
            raise ValueError("Invalid polygon: The given points do not form a valid shape.")
        self.points = points
        self.concave = self._is_concave()
        self.window = window
        self.points_draw = []

        for point in self.points:
            point.convert_coordinates()
        
        self.filled = filled

    def draw(self, painter, viewport) -> None:
        for point in self.points:
            if not point.inside_window:
                return

        # Converte os pontos para o sistema de coordenadas da viewport
        transformed_points = [viewport.transform(p, self.window) for p in self.points_draw]
        
        if self.filled:
            # Cria o polígono preenchido
            polygon = QPolygonF([QPointF(p.x, p.y) for p in transformed_points])
            brush = QBrush(self.color, Qt.BrushStyle.SolidPattern)
            painter.setBrush(brush)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.setPen(QPen(self.color, LINE_THICKNESS))

        for i in range(len(transformed_points)):
            p1 = transformed_points[i]
            p2 = transformed_points[(i + 1) % len(transformed_points)]
            painter.drawLine(int(p1.x), int(p1.y), int(p2.x), int(p2.y))

        if self.filled:
            painter.drawPolygon(QPolygonF([QPointF(p.x, p.y) for p in transformed_points]))

    def _is_concave(self) -> bool:

        def cross_product(p1: Point, p2: Point, p3: Point) -> float:
            return (p2.x - p1.x) * (p3.y - p2.y) - (p2.y - p1.y) * (p3.x - p2.x)

        signs = []
        for i in range(len(self.points)):
            p1, p2, p3 = self.points[i], self.points[(i + 1) % len(self.points)], self.points[(i + 2) % len(self.points)]
            cross = cross_product(p1, p2, p3)
            if cross != 0:
                signs.append(1 if cross > 0 else -1)

        return len(set(signs)) > 1

    def geometric_center(self):
        x_center = 0
        y_center = 0
        for p in self.points:
            x_center += p.x
            y_center += p.y
        x_center /= len(self.points)
        y_center /= len(self.points)
        return int(x_center), int(y_center)
    
    def receive_transform(self, matrix):
        for i in range(len(self.points)):
            point_matrix = np.array([self.points[i].x, self.points[i].y, 1])
            new_point = point_matrix @ matrix
            self.points[i].x = new_point[0]
            self.points[i].y = new_point[1]

    @staticmethod
    def _is_valid_polygon(points: list[Point]) -> bool:
        if len(points) < 3:
            return False
        unique_points = set((p.x, p.y) for p in points)
        if len(unique_points) != len(points):
            return False

        def are_collinear(p1: Point, p2: Point, p3: Point) -> bool:
            return (p2.y - p1.y) * (p3.x - p2.x) == (p3.y - p2.y) * (p2.x - p1.x)

        all_collinear = all(are_collinear(points[0], points[i], points[i + 1]) for i in range(1, len(points) - 1))
        if all_collinear:
            return False
        for i in range(len(points)):
            for j in range(i + 2, len(points) - (i == 0)):
                if Wireframe._lines_intersect(
                    points[i], points[i + 1], 
                    points[j], points[(j + 1) % len(points)]
                ):
                    return False
        return True

    @staticmethod
    def _lines_intersect(p1: Point, p2: Point, p3: Point, p4: Point) -> bool:
        def orientation(a: Point, b: Point, c: Point) -> int:
            val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
            return 0 if val == 0 else (1 if val > 0 else -1)

        o1 = orientation(p1, p2, p3)
        o2 = orientation(p1, p2, p4)
        o3 = orientation(p3, p4, p1)
        o4 = orientation(p3, p4, p2)

        return o1 != o2 and o3 != o4


    def __str__(self):
        return f"{self.name}: Wireframe with {len(self.points)} points"

    def get_points_obj(self):
        points_str = "\n".join(f"v {p.x}, {p.y}" for p in self.points)
        return f"{points_str}\n"
    
    def get_type_obj(self):
        return 'w' if self.filled else 'l'
