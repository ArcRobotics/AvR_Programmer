from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPlainTextEdit
from PySide6.QtGui import QIcon

class CodeView_Window(QDialog):
    def __init__(self, main_window, code, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AVR Programmer")
        Logo=QIcon("ICONS/AppLogo.png")
        self.setWindowIcon(Logo)

        self.setGeometry(100, 100, 640, 480)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Set layout margins to zero
        layout.setSpacing(0)  # Set layout spacing to zero

        # Create a QTextEdit widget
        self.code_edit = QPlainTextEdit()
        self.code_edit.setReadOnly(True)
        layout.addWidget(self.code_edit)

        # Set the code text for the QTextEdit widget
        self.setCode(code)

        self.main_window = main_window

    def setCode(self, code):
        self.code_edit.setPlainText(code)

    def openCodeWindow(self):
        self.show()

