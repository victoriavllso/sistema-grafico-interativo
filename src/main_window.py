from display_file import Display_File
from window import Window
from viewport import Viewport
from PyQt6.QtGui import QPainter, QColor
from point import Point
from line import Line
from wireframe import Wireframe
from PyQt6.QtGui import QPixmap
from utils import *
from gui.gui import Ui_main, QtWidgets
from PyQt6.QtWidgets import QListWidget, QMessageBox



class MainWindow(QtWidgets.QMainWindow, Ui_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        self.display_file = Display_File()
        self.viewport = Viewport()
        self.window = Window()

        self.canvas = QPixmap(self.viewport.x_max - self.viewport.x_min, self.viewport.y_max - self.viewport.y_min)
        self.canvas.fill(QColor("white"))
        self.painter = QPainter(self.canvas)
        self.vp.setPixmap(self.canvas)

        self.display = QListWidget()
        self.display.setGeometry(self.display_file.x_min, self.display_file.y_min, self.display_file.x_max, self.display_file.y_max)
        self.layout().addWidget(self.display)

        # self.create_cartesian_plane()
        
    # Connect signals to slots
    def initUI(self):
        self.create_but.clicked.connect(self.create_object)
        self.delete_but.clicked.connect(self.delete_object)
        self.up.clicked.connect(self.move_window_up)
        self.down.clicked.connect(self.move_window_down)
        self.left.clicked.connect(self.move_window_left)
        self.right.clicked.connect(self.move_window_right)
        self.z_in.clicked.connect(self.zoom_in)
        self.z_out.clicked.connect(self.zoom_out)

    def create_object(self):
        
        points_input = self.points_ln.text().strip()

        # points_input validation
        if not points_input:
            self.show_popup("Erro", "Coordenadas vazias", QMessageBox.Icon.Critical)
            return

        name = self.name_ln.text()

        # name validation
        if name in [obj.name for obj in self.display_file.get_all()]:
            self.show_popup("Erro", "Nome de objeto : Nome ja está em uso", QMessageBox.Icon.Critical)
            return

        points = self.parse_coordinates(points_input)

        # points validation
        if points == []:
            self.show_popup("Erro", "Coordenadas inválidas", QMessageBox.Icon.Critical)
            return
        
        if len(points) > 2 and not name:
            self.show_popup("Erro", "Nome de objeto inválido: O objeto que você deseja criar precisa de um nome", QMessageBox.Icon.Critical)
            return
        
        if len(points) == 2 and not name:
            name = f"obj_{len(self.display_file.get_all())}"

        # Decide which object to create
        if len(points) == 2 and all(isinstance(p, int) for p in points):
            x, y = points[0], points[1]
            obj = Point(name=name, x=x, y=y)

        elif len(points) == 2 and all(isinstance(p, tuple) for p in points):
            x1, y1, x2, y2 = points[0][0], points[0][1], points[1][0], points[1][1]
            point0, point1 = Point(x=x1, y=y1), Point(x=x2, y=y2)
            obj = Line(name= name, point1=point0, point2=point1)

        elif len(points) > 2:
            points = [Point(x=x, y=y) for x, y in points]
            obj = Wireframe(name=name, points=points)
    
        # Add object to display file and update viewport
        self.display_file.add(obj)
        self.update_viewport()


    def parse_coordinates(self, input_text: str) -> list:
        try:
            pontos = list(eval(input_text))
            return pontos
        except Exception:
            return []

    def delete_object(self):
        obj_name = self.name_ln.text().strip()
        self.display_file.remove(obj_name)
        self.update_viewport()

    def move_window_up(self):
        self.window.up()
        self.update_viewport()

    def move_window_down(self):
        self.window.down()
        self.update_viewport()

    def move_window_left(self):
        self.window.left()
        self.update_viewport()

    def move_window_right(self):
        self.window.right()
        self.update_viewport()

    def zoom_in(self):
        self.window.z_in()
        self.update_viewport()

    def zoom_out(self):
        self.window.z_out()
        self.update_viewport()

    def update_viewport(self):
        self.canvas.fill(QColor("white"))
        self.painter.begin(self.canvas)
        for obj in self.display_file.get_all():
            obj.draw(self.painter, self.viewport, self.window)
        self.painter.end()
        self.vp.setPixmap(self.canvas)
        self.update_display()

    def update_display(self):
        self.display.clear()
        self.display.addItem("Objetos:")
        for obj in self.display_file.get_all():
            self.display.addItem(f"{obj.name} - {obj.__class__.__name__}")
        self.display.show()

    def create_cartesian_plane(self, center_x = 500, center_y = -500, size = 1000):
        # use center_x and center_y to create the cartesian plane
        r1 = Line("x_axis", Point(center_x - size, center_y), Point(center_x + size, center_y))
        r2 = Line("y_axis", Point(center_x, center_y - size), Point(center_x, center_y + size))

        self.display_file.add(r1)
        self.display_file.add(r2)
        self.update_viewport()

    def show_popup(self, title:str = "standart", message:str = "standart", icon:QMessageBox.Icon = QMessageBox.Icon.Information):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
