from display_file import Display_File
from window import Window
from viewport import Viewport
from PyQt6.QtGui import QPainter, QColor
from point import Point
from line import Line
from wireframe import Wireframe
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from utils import *
from gui import Ui_main, QtWidgets

import re


class MainWindow(QtWidgets.QMainWindow, Ui_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self) # Inicializa a interface gráfica
        self.initUI() # Conecta sinais a slots
        self.display_file = Display_File()
        self.viewport = Viewport()
        self.window = Window()
        self.canvas = QPixmap(self.viewport.width, self.viewport.height)
        self.canvas.fill(QColor("white"))
        self.painter = QPainter(self.canvas)
        self.vp.setPixmap(self.canvas) # atribui a imagem ao label
        
     
    
    # Connect signals to slots
    def initUI(self): # depois de iniciar a interface, conectamos os botões aos slots
        self.create_but.clicked.connect(self.create_object)
        self.delete_but.clicked.connect(self.delete_object)
        self.up.clicked.connect(self.move_window_up)
        self.down.clicked.connect(self.move_window_down)
        self.left.clicked.connect(self.move_window_left)
        self.right.clicked.connect(self.move_window_right)
        self.z_in.clicked.connect(self.zoom_in)
        self.z_out.clicked.connect(self.zoom_out)
        
       
      
     

    # Create object from input
    def create_object(self):
        # Input
        text = self.points_ln.text().strip()
        if not text:
            return
        
        points = self.parse_coordinates(text)

        # Decide which object to create
        if len(points) == 1:
            obj = Point(*points[0])
        elif len(points) == 2:
            obj = Line(points[0], points[1])
        else:
            obj = Wireframe([Point(x, y) for x, y in points])
    
        # Add object to display file and update viewport
        self.display_file.add(obj)
        self.update_viewport()

    def parse_coordinates(self, input_text: str) -> list:
        points = []

        try:
            # Remove espaços extras e divide a string em pares de coordenadas
            pairs = input_text.strip().split("),")
            for pair in pairs:
                # Remove os parênteses e espaços extras
                pair = pair.strip("(), ")
                if not pair:
                    continue  # Ignora pares vazios
                # Divide a string em componentes x e y
                x, y = pair.split(",")
                # Remove espaços extras e converte para float
                x = float(x.strip())
                y = float(y.strip())
                points.append((x, y))

        except ValueError:
            raise ValueError(f"Formato de coordenadas inválido: {input_text}. Certifique-se de usar o formato '(x1, y1), (x2, y2), ...'.")
        
        return points

    # Delete object from display file
    def delete_object(self):
        pass
        obj_name = self.delete_line.text().strip()
        self.display_file.remove(obj_name)
        self.update_viewport()
    # Move window up
    def move_window_up(self):

        self.update_viewport()

    # Move window down
    def move_window_down(self):

        self.update_viewport()

    # Move window left
    def move_window_left(self):

        self.update_viewport()

    # Move window right
    def move_window_right(self):

        self.update_viewport()

    # Zoom in
    def zoom_in(self):

        self.update_viewport()

    # Zoom out
    def zoom_out(self):

        self.update_viewport()

    # Update viewport
    def update_viewport(self):
        self.canvas.fill(QColor("white"))
        self.painter.begin(self.canvas)
        
        for obj in self.display_file.get_all():
            obj.draw(self.viewport, self.window)
        self.painter.end()
        #self.view.setPixmap(self.canvas)
    
    def draw_objects(self):
        """
        Desenha todos os objetos armazenados na cena gráfica.
        """


        for obj in self.objects:
            if isinstance(obj, Point) or isinstance(obj, Line) or isinstance(obj, Wireframe):
                obj.draw(self.painter, self.viewport, self.window)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
