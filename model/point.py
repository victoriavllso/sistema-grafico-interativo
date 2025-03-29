from model.graphic_object import GraphicObject
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt
from model.utils import POINT_THICKNESS


class Point(GraphicObject):
    def __init__(self, x: int, y: int, name="default"):
        super().__init__(name)
        self.x = x
        self.y = y

    def draw(self, painter, viewport, window):
        # Apply the viewport transformation
        transformed_point = viewport.transform(self, window)

        x, y = int(transformed_point.x), int(transformed_point.y)

        painter.setPen(QPen(Qt.GlobalColor.green, POINT_THICKNESS))
        painter.drawPoint(x, y)
            # ---------- DONE ---------- #
    def geometric_center(self):
        return self.x, self.y