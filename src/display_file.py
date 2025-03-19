from graphic_object import GraphicObject
from window import Window
from utils import X_MAX, X_MIN, Y_MAX, Y_MIN

class Display_File:
    def __init__(self):
        self.list = []
        self.window = Window(X_MIN, X_MAX, Y_MIN, Y_MAX)

    def add(self, graphic_object: GraphicObject) -> None:
        self.list.append(graphic_object)

    def remove(self, name: str) -> None:
        for obj in self.list:
            if obj.name == name:
                self.list.remove(obj)
    
    def get_all(self) -> list:
        return self.list

            # ---------- DONE ---------- #
