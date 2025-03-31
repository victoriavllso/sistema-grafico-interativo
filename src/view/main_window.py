from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtGui import QPixmap
from src.model.utils import *
from src.view.gui import Ui_main, QtWidgets
from PyQt6.QtWidgets import QListWidget, QColorDialog
from src.controller.controller import Controller
from PyQt6.QtCore import Qt

class MainWindow(QtWidgets.QMainWindow, Ui_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        self.controller = Controller(self)
        self.canvas = QPixmap(self.controller.viewport.x_max - self.controller.viewport.x_min, self.controller.viewport.y_max - self.controller.viewport.y_min)
        self.canvas.fill(QColor("white"))
        self.painter = QPainter(self.canvas)
        self.vp.setPixmap(self.canvas)

        self.color = QColor("black")

        # Display
        self.display = QListWidget()
        self.display.setGeometry(self.controller.display_file.x_min, self.controller.display_file.y_min, self.controller.display_file.x_max, self.controller.display_file.y_max)
    
        # Display properties
        self.display.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.display.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.display.setMinimumHeight(150)
        self.display.setMinimumWidth(200)
        self.layout().addWidget(self.display)

    # Connect signals to slots
    def initUI(self):
        self.create_but.clicked.connect(self.create_object)
        self.delete_but.clicked.connect(self.delete_object)
        self.up.clicked.connect(lambda: self.controller.move_window("up"))
        self.down.clicked.connect(lambda: self.controller.move_window("down"))
        self.left.clicked.connect(lambda: self.controller.move_window("left"))
        self.right.clicked.connect(lambda: self.controller.move_window("right"))
        self.z_in.clicked.connect(lambda: self.controller.zoom("in"))
        self.z_out.clicked.connect(lambda: self.controller.zoom("out"))
        self.transform_button.clicked.connect(lambda: self.controller.open_transform_window())
        self.color_button.clicked.connect(self.open_color_dialog)
    
    def create_object(self):
        self.controller.create_object()

    def delete_object(self):
        obj_name = self.name_ln.text().strip()
        self.controller.delete_object(obj_name)
    
    def update_viewport(self):
        self.canvas.fill(QColor("white"))
        if self.painter.isActive():
            self.painter.end()
        self.painter.begin(self.canvas)
        self.controller.draw_objects(self.painter)
        self.painter.end()
        self.vp.setPixmap(self.canvas)
        self.update_display()

    def update_display(self):
        self.display.clear()
        self.display.addItem("Objetos: \n")
        for obj in self.controller.display_file.get_all():
            self.display.addItem(f"{obj.name} - {obj.__class__.__name__}")
        self.display.show()
    
    def get_object(self):
        self.controller.update_selected_object()

    def open_color_dialog(self):
        self.color = QColorDialog.getColor()
        