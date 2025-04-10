from src.model.graphic_objects.graphic_object import GraphicObject
from src.utils.utils import DF_X_MIN, DF_Y_MIN, DF_X_MAX, DF_Y_MAX
from src.model.display.display import Display
from typing import Type

class DisplayFile(Display):
    def __init__(self, x_min: int = DF_X_MIN, y_min: int = DF_Y_MIN, x_max: int = DF_X_MAX, y_max: int = DF_Y_MAX):
        super().__init__(x_min, y_min, x_max, y_max)

    def get_next_possible_name(self) -> int:
        """Get the next possible name for an object"""
        return f"obj_{len(self.list) + 1}"
    
    def remove(self, name: str) -> None:
        """Remove an object from the display list by name"""
        for obj in self.list:
            if obj.name == name:
                self.list.remove(obj)

    def verify_name(self, name: str) -> bool:
        """Verifica se o nome já existe na lista de objetos gráficos"""
        for obj in self.list:
            if obj.name == name:
                return True
        return False