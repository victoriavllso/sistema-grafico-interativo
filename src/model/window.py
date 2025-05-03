from src.utils.utils import STEP, PERCENTAGE, W_X_MIN, W_X_MAX, W_Y_MIN, W_Y_MAX, W_Z_MIN, W_Z_MAX
import numpy as np
class Window:
    def __init__(self, x_min = W_X_MIN, x_max = W_X_MAX, y_min = W_Y_MIN, y_max = W_Y_MAX, Z_min = W_Z_MIN, Z_max = W_Z_MAX):
        self.x_min = x_min        
        self.x_max = x_max
        self.y_min = y_min        
        self.y_max = y_max
        self.z_min = Z_min
        self.z_max = Z_max
        self.vpn = (0, 0, 1) # x = 0, y = 0, z = 1 
        self.direction = (1, 0, 0) # x = 0, y = 1
        self.view_up = (0,1,0) # x = 0, y = 1, z = 0

        """
        Antes da rotação:
        ↑   (viewup = (0, 1))

        Depois de girar 90° para a direita:
        →   (viewup = (1, 0))

        Depois de girar 90° para a esquerda:
        ←   (viewup = (-1, 0))
        """

    def up(self, step:int = STEP) -> None:
        """Move the window up by a given step size."""
        self.y_min += step
        self.y_max += step
    
    def down(self, step:int = STEP) -> None:
        """Move the window down by a given step size."""
        self.y_min -= step
        self.y_max -= step
    
    def left(self, step:int = STEP) -> None:
        """Move the window left by a given step size."""
        self.x_min -= step
        self.x_max -= step

    def right(self, step:int = STEP) -> None:
        """Move the window right by a given step size."""
        self.x_min += step
        self.x_max += step

    def z_in(self, percentage:int = PERCENTAGE) -> None:
        """Zoom in the window by a given percentage."""
        self.x_min /= percentage/100 + 1
        self.x_max /= percentage/100 + 1
        self.y_min /= percentage/100 + 1
        self.y_max /= percentage/100 + 1

    def z_out(self, percentage:int = PERCENTAGE) -> None:
        """Zoom out the window by a given percentage."""
        self.x_min *= percentage/100 + 1
        self.x_max *= percentage/100 + 1
        self.y_min *= percentage/100 + 1
        self.y_max *= percentage/100 + 1
       

    def get_center(self) -> tuple:
        """Calculate the center of the window."""
        return self.x_min, self.y_min, self.z_min
    def get_min(self) -> tuple:
        """Get the minimum coordinates of the window."""
        return self.x_min, self.y_min, self.z_min
    def get_max(self) -> tuple:
        """Get the maximum coordinates of the window."""
        return self.x_max, self.y_max, self.z_max

    def transform_vector(self, actual_direction:np.ndarray, rotarion_matrix:np.ndarray) -> np.ndarray:
        """Transform the direction vector using a rotation matrix."""
        aux = actual_direction/ np.linalg.norm(actual_direction)
        result = np.dot(rotarion_matrix, aux)
        return result
    
    #def rotate(self, angle):
    #    """Rotate the window by a given angle."""
    #    actual_direction = np.array(self.direction)
    #    radians = angle * np.pi / 180
    #    cos = np.cos(radians)
    #    sin = np.sin(radians)
    #    rotation_matrix = [[cos, -sin], 
    #                       [sin, cos]]
    #    rotate = self.transform_vector(actual_direction, rotation_matrix)
    #    self.direction = (rotate[0], rotate[1])

    def rotate_vector(self, vector, angle:int, axis = 'z') -> None:
        radians = np.radians(angle)
        cos = np.cos(radians)
        sin = np.sin(radians)

        if axis == 'x':
            matrix = np.array([[1, 0, 0],
                                [0, cos, -sin],
                                [0, sin, cos]])
            
        elif axis == 'y':
            matrix = np.array([[cos, 0, sin],
                                [0, 1, 0],
                                [-sin, 0, cos]])
        elif axis == 'z':
            matrix = np.array([[cos, -sin, 0],
                                [sin, cos, 0],
                                [0, 0, 1]])
        else:
            raise ValueError("Eixo inválido. Use 'x', 'y' ou 'z'.")
        
        rotated_vector = np.dot(matrix, vector)
        return rotated_vector

    def rotate_window_left(self, angle:int) -> None:
        """Rotate the window to the left by a given angle."""
        self.direction = self.rotate_vector(self.direction, -angle, axis='z')
        self.view_up = self.rotate_vector(self.view_up, angle, axis='z')

        
    def rotate_window_right(self, angle:int) -> None:
        """Rotate the window to the right by a given angle.""" 
        actual_direction = np.array(self.direction)
        radians = angle * np.pi / 180
        cos = np.cos(radians)
        sin = np.sin(radians)
        rotation_matrix = [[cos, -sin], 
                           [sin, cos]]
        rotate = self.transform_vector(actual_direction, rotation_matrix)
        self.direction = (rotate[0], rotate[1])
    
    def get_vrp(self):
        return self.get_center()
    
    def get_vpn(self):
        return self.vpn