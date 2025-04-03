from src.model.display.display import Display
from src.utils.utils import DT_X_MAX, DT_X_MIN, DT_Y_MAX, DT_Y_MIN


class DisplayTransform(Display):
    def __init__(self, x_min=DT_X_MIN, y_min=DT_Y_MIN, x_max=DT_X_MAX, y_max=DT_Y_MAX):
        super().__init__(x_min, y_min, x_max, y_max)
