from src.view.main_window import MainWindow
from PyQt6 import QtWidgets
import os
import atexit

# Função para limpar o cache de __pycache__
def clean_cache():
    os.system("find . -type d -name '__pycache__' -exec rm -r {} +")

# Registrar a função de limpeza para ser chamada quando a aplicação for fechada
atexit.register(clean_cache)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
