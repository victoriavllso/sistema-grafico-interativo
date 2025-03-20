from graphic_object import GraphicObject
from PyQt6.QtGui import QPen, QColor


class Point(GraphicObject):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y

    def draw(self, painter, viewport, window):
        # Aplica a transformação para obter a posição correta na viewport
        transformed_point = viewport.transform(self, window)

        x, y = int(transformed_point.x), int(transformed_point.y)

        # Define a cor e desenha o ponto
        painter.setPen(QPen(QColor(255, 0, 0), 5))  # Define espessura 5 para visibilidade
        painter.drawPoint(x, y)
        print(f"Ponto desenhado em ({x}, {y})")

