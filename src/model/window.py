from src.utils.utils import STEP, PERCENTAGE, W_X_MIN, W_X_MAX, W_Y_MIN, W_Y_MAX
import numpy as np
class Window:
    def __init__(self, x_min = W_X_MIN, x_max = W_X_MAX, y_min = W_Y_MIN, y_max = W_Y_MAX):
        self.x_min = x_min        
        self.x_max = x_max
        self.y_min = y_min        
        self.y_max = y_max
        self.direction = (0,1) # x = 0, y = 1
        """
        Antes da rotação:
        ↑   (viewup = (0, 1))

        Depois de girar 90° para a direita:
        →   (viewup = (1, 0))

        Depois de girar 90° para a esquerda:
        ←   (viewup = (-1, 0))
        """

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

    def get_center(self):
        return self.x_min, self.y_min

    def transform_vector(self, actual_direction, rotarion_matrix):
        aux = actual_direction/ np.linalg.norm(actual_direction)
        result = np.dot(rotarion_matrix, aux)
        return result

    def rotate_window_left(self, angle): # inserir campo para o angulo de rotação da window
        angle *= -1 # gira no sentido anti horário

        actual_direction = np.array(self.direction)

        radians = angle * np.pi / 180

        cos = np.cos(radians)
        sin = np.sin(radians)
        rotation_matrix = [[cos, -sin], 
                           [sin, cos]]

        rotate = self.transform_vector(actual_direction, rotation_matrix)
        self.direction = (rotate[0], rotate[1])

    def rotate_window_right(self, angle): 
        actual_direction = np.array(self.direction)

        radians = angle * np.pi / 180
        cos = np.cos(radians)
        sin = np.sin(radians)

        rotation_matrix = [[cos, -sin], 
                           [sin, cos]]
        rotate = self.transform_vector(actual_direction, rotation_matrix)
        self.direction = (rotate[0], rotate[1])