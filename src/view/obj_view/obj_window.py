from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QPushButton, QFileDialog, QTextEdit
)
import sys
from src.model.descritor_obj import DescritorOBJ

class OBJDialog(QDialog):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.setWindowTitle("Manipulador de Arquivos OBJ")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        # Botões
        self.btn_carregar = QPushButton("Carregar .obj")
        self.btn_salvar = QPushButton("Salvar .obj")

        # Área de texto para exibir conteúdo
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)

        # Adiciona os elementos na UI
        self.layout.addWidget(self.btn_carregar)
        self.layout.addWidget(self.btn_salvar)
        self.layout.addWidget(self.text_area)

        self.setLayout(self.layout)

        # Conectar os botões aos métodos
        self.btn_carregar.clicked.connect(self.controller.import_obj)
        self.btn_salvar.clicked.connect(self.controller.export_obj)

        # Inicializa o objeto
        self.objeto = None

    def select_file(self) -> str:
        """Retorna o caminho do arquivo .obj"""
        file_name, _ = QFileDialog.getOpenFileName(self, "Carregar Arquivo OBJ", "", "Arquivos OBJ (*.obj);;Todos os Arquivos (*)")
        
        return file_name
