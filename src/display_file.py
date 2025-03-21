from graphic_object import GraphicObject
from utils import DF_X1, DF_X2, DF_Y1, DF_Y2
class Display_File:
    def __init__(self, x1 = DF_X1, y1 = DF_Y1, x2 = DF_X2, y2 = DF_Y2):
        self.list = []
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def add(self, graphic_object: GraphicObject) -> None:
        self.list.append(graphic_object)

    def remove(self, name: str) -> None:
        for obj in self.list:
            if obj.name == name:
                self.list.remove(obj)
    
    def get_all(self) -> list:
        return self.list

            # ---------- DONE ---------- #
