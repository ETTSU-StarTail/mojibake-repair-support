import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文字化け復旧支援ツール")
        layout = QVBoxLayout()
        # ...UI部品は後続で追加...
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
