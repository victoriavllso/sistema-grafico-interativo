from model.graphic_object import GraphicObject
from model.point import Point
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt
from model.utils import LINE_THICKNESS

class Wireframe(GraphicObject):
    def __init__(self, name, points: list[Point]):
        super().__init__(name)
        
        # Verify if the given points form a valid polygon
        if not self._is_valid_polygon(points):
            raise ValueError("Invalid polygon: The given points do not form a valid shape.")

        self.points = points

        # Check if the polygon is concave
        self.concave = self._is_concave()

    def draw(self, painter, viewport, window) -> None:
        painter.setPen(QPen(Qt.GlobalColor.blue, LINE_THICKNESS))
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            p1 = viewport.transform(p1, window)
            p2 = viewport.transform(p2, window)
            painter.drawLine(int(p1.x), int(p1.y), int(p2.x), int(p2.y))

    def _is_concave(self) -> bool:
        def cross_product(p1: Point, p2: Point, p3: Point) -> float:
            return (p2.x - p1.x) * (p3.y - p2.y) - (p2.y - p1.y) * (p3.x - p2.x)

        signs = []
        for i in range(len(self.points)):
            p1, p2, p3 = self.points[i], self.points[(i + 1) % len(self.points)], self.points[(i + 2) % len(self.points)]
            cross = cross_product(p1, p2, p3)
            
            if cross != 0:  # Ignore collinear points
                signs.append(1 if cross > 0 else -1)

        return len(set(signs)) > 1  # If there are more than one sign, the polygon is concave

        # ---------- STATIC METHODS ---------- #

    @staticmethod
    def _is_valid_polygon(points: list[Point]) -> bool:
        if len(points) < 3:
            return False

        unique_points = set((p.x, p.y) for p in points)
        if len(unique_points) != len(points):
            return False

        # Verifica se os pontos são colineares
        def are_collinear(p1: Point, p2: Point, p3: Point) -> bool:
            return (p2.y - p1.y) * (p3.x - p2.x) == (p3.y - p2.y) * (p2.x - p1.x)

        all_collinear = all(are_collinear(points[0], points[i], points[i + 1]) for i in range(1, len(points) - 1))
        if all_collinear:
            return False

        # Verifica interseção entre arestas não adjacentes
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

        # ---------- STATIC METHODS ---------- #

            # ---------- DONE ---------- #
    def geometric_center(self):
        
        for p in self.points:
            x_center += p.x
            y_center += p.y
        x_center /= len(self.points)
        y_center /= len(self.points)
        return x_center, y_center