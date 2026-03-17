import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPlainTextEdit, QComboBox
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文字化け復旧支援ツール")
        self.setGeometry(100, 100, 1000, 600)
        
        main_layout = QVBoxLayout()
        
        # 入力欄セクション
        input_section = self._create_input_section()
        main_layout.addLayout(input_section)
        
        self.setLayout(main_layout)
    
    def _create_input_section(self):
        """入力欄＆文字コード選択UIを生成"""
        layout = QVBoxLayout()
        
        # テキスト入力欄
        layout.addWidget(QLabel("入力文字列:"))
        self.text_input = QPlainTextEdit()
        self.text_input.setPlaceholderText("文字化けした文字列をここに入力してください")
        layout.addWidget(self.text_input)
        
        # 見ている文字コード選択欄
        codec_layout = QHBoxLayout()
        codec_layout.addWidget(QLabel("見ている文字コード:"))
        self.current_codec = QComboBox()
        self.current_codec.addItems([
            "UTF-8",
            "UTF-8-SIG (UTF-8 with BOM)",
            "Shift_JIS",
            "CP932",
            "EUC-JP",
            "ISO-2022-JP",
            "UTF-16LE",
            "UTF-16BE",
        ])
        codec_layout.addWidget(self.current_codec)
        codec_layout.addStretch()
        layout.addLayout(codec_layout)
        
        return layout

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
