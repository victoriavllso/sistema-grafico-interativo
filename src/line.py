from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt
from graphic_object import GraphicObject


class Line(GraphicObject):
    def __init__(self, point1, point2):
        super().__init__()
        self.point1 = point1
        self.point2 = point2

    def draw(self, painter, viewport, window):
        """
        Desenha a linha na cena usando QGraphicsLineItem.
        """
        # Transforma os pontos para a viewport
        transformed_p1 = viewport.transform(self.point1, window)
        transformed_p2 = viewport.transform(self.point2, window)

  
        painter.drawLine(transformed_p1.x, transformed_p1.y, transformed_p2.x, transformed_p2.y)


        # Adiciona o item à cena
        print("linha desenhada")