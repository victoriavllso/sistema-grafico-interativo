from graphic_object import GraphicObject
from point import Point
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt

class Wireframe(GraphicObject):
    def __init__(self, points: list[Point], name: str = "Wireframe"):
        super().__init__(name)
        
        # Verify if the given points form a valid polygon
        if not self._is_valid_polygon(points):
            raise ValueError("Invalid polygon: The given points do not form a valid shape.")

        self.points = points
        # Check if the polygon is concave
        self.concave = self._is_concave()

    def draw(self, painter) -> None:
        painter.setPen(QPen(Qt.GlobalColor.green, 2))
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            painter.drawLine(int(p1.x), int(p1.y), int(p2.x), int(p2.y))

    @staticmethod
    def _is_valid_polygon(points: list[Point]) -> bool:
        if len(points) < 3:
            return False

        unique_points = set((p.x, p.y) for p in points)
        if len(unique_points) != len(points):
            return False

        for i in range(len(points)):
            for j in range(i + 2, len(points) - (i == 0)):
                if Wireframe._lines_intersect(
                    points[i], points[i + 1], 
                    points[j], points[(j + 1) % len(points)]
                ):
                    return False

        return True

    def _is_concave(self) -> bool:
        orientations = []
        for i in range(len(self.points)):
            p1, p2, p3 = self.points[i], self.points[(i + 1) % len(self.points)], self.points[(i + 2) % len(self.points)]
            orientations.append(self._orientation(p1, p2, p3))

        return any(o != orientations[0] for o in orientations if o != 0)

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
