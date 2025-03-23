from utils import STEP, PERCENTAGE, W_X_MIN, W_X_MAX, W_Y_MIN, W_Y_MAX

class Window:
    def __init__(self, x_min = W_X_MIN, x_max = W_X_MAX, y_min = W_Y_MIN, y_max = W_Y_MAX):
        self.x_min = x_min        
        self.x_max = x_max
        self.y_min = y_min        
        self.y_max = y_max

    def up(self, step = STEP):
        self.y_min += step
        self.y_max += step
    
    def down(self, step = STEP):
        self.y_min -= step
        self.y_max -= step
    
    def left(self, step = STEP):
        self.x_min -= step
        self.x_max -= step

    def right(self, step = STEP):
        self.x_min += step
        self.x_max += step

    def z_in(self, percentage = PERCENTAGE):
        self.x_min /= percentage/100 + 1
        self.x_max /= percentage/100 + 1
        self.y_min /= percentage/100 + 1
        self.y_max /= percentage/100 + 1

    def z_out(self, percentage = PERCENTAGE):
        self.x_min *= percentage/100 + 1
        self.x_max *= percentage/100 + 1
        self.y_min *= percentage/100 + 1
        self.y_max *= percentage/100 + 1

        # ---------- DONE ---------- #
