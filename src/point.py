from PyQt6.QtCore import Qt
from graphic_object import GraphicObject


class Point(GraphicObject):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y

    def draw(self, painter, viewport, window):
        """
        Desenha o ponto na tela usando QPainter.
        """
        # Aplica a transformação para obter a posição correta na viewport
        transformed_point = viewport.transform(self, window)
        painter.drawPoint(transformed_point.x, transformed_point.y)
        print("ponto desenhado")