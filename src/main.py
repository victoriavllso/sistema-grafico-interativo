from display_file import Display_File
from window import Window
from viewport import Viewport
from PyQt6.QtGui import QPainter, QColor
from point import Point
from line import Line
from wireframe import Wireframe
from PyQt6.QtGui import QPixmap
from utils import *
from gui import Ui_main, QtWidgets
from PyQt6.QtWidgets import QListWidget, QMessageBox



class MainWindow(QtWidgets.QMainWindow, Ui_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        self.display_file = Display_File()
        self.viewport = Viewport()
        self.window = Window()

        self.canvas = QPixmap(self.viewport.width, self.viewport.height)
        self.canvas.fill(QColor("white"))
        self.painter = QPainter(self.canvas)
        self.vp.setPixmap(self.canvas)

        self.display = QListWidget()
        self.display.setGeometry(self.display_file.x1, self.display_file.y1, self.display_file.x2, self.display_file.y2)
        self.layout().addWidget(self.display)
        
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
        text = self.points_ln.text().strip()
        name = self.name_ln.text()
        if not text:
            return
        
        points = self.parse_coordinates(text)

        if points == []:
            return

        # Decide which object to create
        if len(points) == 1:
            x, y = points[0]
            if not name:
                name = f"ponto_{len(self.display_file.get_all())}"
            obj = Point(name=name, x=x, y=y)
        elif len(points) == 2 and name and name not in [obj.name for obj in self.display_file.get_all()]:
            x1, y1 = points[0]
            x2, y2 = points[1]
            point0 = Point(x=x1, y=y1)
            point1 = Point(x=x2, y=y2)
            obj = Line(name= name, point1=point0, point2=point1)
        elif len(points) > 2 and name and name not in [obj.name for obj in self.display_file.get_all()]:
            vet_points = [Point(*p) for p in points]
            obj = Wireframe(name=name, points=vet_points)
        elif name in [obj.name for obj in self.display_file.get_all()]:
            self.show_popup("Erro", "Nome de objeto já existente", QMessageBox.Icon.Critical)
            return
        elif name == "":
            self.show_popup("Erro", "O nome desse objeto não pode ser vazio", QMessageBox.Icon.Critical)
            return
        else:
            return
    
        # Add object to display file and update viewport
        self.display_file.add(obj)
        self.update_viewport()


    def parse_coordinates(self, input_text: str) -> list:
        points = []

        try:
            pairs = input_text.strip().split("),")
            for pair in pairs:
                pair = pair.strip("(), ")
                if not pair:
                    continue
                x, y = pair.split(",")
                x = float(x.strip())
                y = float(y.strip())
                points.append((x, y))

        except ValueError:
            self.show_popup("Erro", "Coordenadas inválidas", QMessageBox.Icon.Critical)
            return []
        return points

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

    def show_popup(self, title:str = "standart", message:str = "standart", icon:QMessageBox.Icon = QMessageBox.Icon.Information):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
