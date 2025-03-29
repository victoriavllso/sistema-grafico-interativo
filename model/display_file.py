from model.graphic_object import GraphicObject
from model.utils import DF_X_MIN, DF_Y_MIN, DF_X_MAX, DF_Y_MAX
class DisplayFile:
    def __init__(self, x_min: int = DF_X_MIN, y_min: int = DF_Y_MIN, x_max: int = DF_X_MAX, y_max: int = DF_Y_MAX):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.list = []

    def add(self, graphic_object: GraphicObject) -> None:
        self.list.append(graphic_object)

    def remove(self, name: str) -> None:
        for obj in self.list:
            if obj.name == name:
                self.list.remove(obj)
    
    def get_all(self) -> list:
        return self.list

    def get_selected_object(self, name: str):
        for obj in self.list:
            if obj.name == name:
                return obj
            # ---------- DONE ---------- #
#562b00