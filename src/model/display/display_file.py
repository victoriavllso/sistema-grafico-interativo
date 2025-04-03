from src.model.graphic_objects.graphic_object import GraphicObject
from src.utils.utils import DF_X_MIN, DF_Y_MIN, DF_X_MAX, DF_Y_MAX
from src.model.display.display import Display
class DisplayFile(Display):
    def __init__(self, x_min: int = DF_X_MIN, y_min: int = DF_Y_MIN, x_max: int = DF_X_MAX, y_max: int = DF_Y_MAX):
        super().__init__(x_min, y_min, x_max, y_max)
            
    def get_num_points(self) -> int:
        cont = 0
        for obj in self.list:
            if obj.name.startswith("point_"):
                cont += 1
        return cont
