from PyQt6.QtWidgets import QMessageBox, QFileDialog, QWidget

class GUIUtils:
    """Classe com utilitários para a interface gráfica."""

    @staticmethod
    def show_popup(title="Aviso", message="Mensagem", icon=QMessageBox.Icon.Information):
        """Exibe um popup com título, mensagem e ícone especificados."""
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    @staticmethod
    def show_error_popup(message="Ocorreu um erro"):
        """Exibe um popup de erro."""
        GUIUtils.show_popup("Erro", message, QMessageBox.Icon.Critical)

    @staticmethod
    def show_warning_popup(message="Aviso importante"):
        """Exibe um popup de aviso."""
        GUIUtils.show_popup("Aviso", message, QMessageBox.Icon.Warning)

    @staticmethod
    def open_file_dialog(parent: QWidget = None, filter_text="Todos os Arquivos (*.*)"):
        """Abre uma caixa de diálogo para seleção de arquivos e retorna o caminho do arquivo escolhido."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(parent, "Selecionar Arquivo", "", filter_text)
        return file_path if file_path else None

    @staticmethod
    def save_file_dialog(parent: QWidget = None, filter_text="Todos os Arquivos (*.*)"):
        """Abre uma caixa de diálogo para salvar arquivos e retorna o caminho escolhido."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(parent, "Salvar Arquivo", "", filter_text)
        return file_path if file_path else None
