import sys
from functools import partial
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPlainTextEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QHeaderView
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

        # 出力一覧セクション
        output_section = self._create_output_section()
        main_layout.addLayout(output_section)

        # 任意文字コード追加セクション
        custom_codec_section = self._create_custom_codec_section()
        main_layout.addLayout(custom_codec_section)

        self.setLayout(main_layout)

        # プラットフォーム別のデフォルト文字コード設定
        self._set_default_codec_for_platform()

        # シグナル接続
        self._connect_signals()

    def _set_default_codec_for_platform(self):
        """OSに応じたデフォルト文字コードを設定"""
        if sys.platform.startswith("win"):
            self.current_codec.setCurrentText("Shift_JIS")

    def _connect_signals(self):
        """ボタンクリックなどのシグナルをスロットに接続"""
        self.execute_btn.clicked.connect(self._on_execute_clicked)
        self.add_codec_btn.clicked.connect(self._on_add_codec_clicked)

    def _on_execute_clicked(self):
        """「復元候補を生成」ボタンが押された時の処理"""
        text = self.text_input.toPlainText()
        codec_name = self.current_codec.currentText()

        if not text:
            return

        # 正規化した文字コード名を取得
        normalized_codec = self._normalize_codec_name(codec_name)

        try:
            # 入力文字列を指定の文字コードでバイト列に変換
            byte_data = text.encode(normalized_codec)
        except (UnicodeEncodeError, LookupError):
            # エラーでバイト列化できない場合
            self.output_table.setRowCount(0)
            return

        # バイト列を各文字コードで復元
        results = self.decode_with_all_codecs(byte_data)

        # テーブルに結果を表示
        self.output_table.setRowCount(len(results))
        self.output_table.setColumnCount(3)
        self.output_table.setHorizontalHeaderLabels(["文字コード", "復元結果", "操作"])
        for row, (codec, decoded_text) in enumerate(results):
            self.output_table.setItem(row, 0, QTableWidgetItem(codec))
            self.output_table.setItem(row, 1, QTableWidgetItem(decoded_text))

            copy_btn = QPushButton("📋")
            copy_btn.setToolTip("この復元結果をコピー")
            copy_btn.setFixedWidth(40)
            copy_btn.clicked.connect(partial(self._copy_text_to_clipboard, decoded_text))
            self.output_table.setCellWidget(row, 2, copy_btn)

    def _copy_text_to_clipboard(self, text: str):
        """指定文字列をクリップボードにコピー"""
        QApplication.clipboard().setText(text)

    def _on_add_codec_clicked(self):
        """「追加」ボタンが押された時の処理（カスタム文字コード追加）"""
        custom_codec = self.custom_codec_input.text().strip()
        if not custom_codec:
            return

        # コンボボックスに追加（重複チェック）
        if self.current_codec.findText(custom_codec) == -1:
            self.current_codec.addItem(custom_codec)

        self.custom_codec_input.clear()

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

    def _create_output_section(self):
        """出力一覧（テーブル）UIを生成"""
        layout = QVBoxLayout()

        layout.addWidget(QLabel("復元候補（可能性のある文字コード）:"))

        # テーブルウィジェット
        self.output_table = QTableWidget()
        self.output_table.setColumnCount(3)
        self.output_table.setHorizontalHeaderLabels(["文字コード", "復元結果", "操作"])
        header = self.output_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        layout.addWidget(self.output_table)

        # 実行ボタン
        button_layout = QHBoxLayout()
        self.execute_btn = QPushButton("復元候補を生成")
        button_layout.addWidget(self.execute_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        return layout

    def _create_custom_codec_section(self):
        """任意文字コード追加UIを生成"""
        layout = QHBoxLayout()

        layout.addWidget(QLabel("カスタム文字コード（追加するコード名）:"))
        self.custom_codec_input = QLineEdit()
        self.custom_codec_input.setPlaceholderText("例: utf-32, iso-8859-1")
        layout.addWidget(self.custom_codec_input)

        self.add_codec_btn = QPushButton("追加")
        layout.addWidget(self.add_codec_btn)

        return layout

    def _normalize_codec_name(self, codec_name: str) -> str:
        """Pythonの文字コード名に正規化（例：UTF-8 → utf-8）"""
        # -SIG (BOM付き) を utf-8-sig に変換
        if "SIG" in codec_name or "BOM" in codec_name:
            return "utf-8-sig"
        return codec_name.lower().replace(" ", "-")

    def _get_available_codecs(self) -> list:
        """主要な文字コード一覧を取得"""
        return [
            "utf-8",
            "utf-8-sig",
            "shift_jis",
            "cp932",
            "euc_jp",
            "iso2022_jp",
            "utf_16_le",
            "utf_16_be",
            "utf_32",
            "iso8859_1",
            "ascii",
        ]

    def decode_with_all_codecs(self, byte_data: bytes) -> list:
        """
        バイト列を様々な文字コードで復元を試みる

        Args:
            byte_data: バイト列

        Returns:
            [(文字コード名, 復元結果), ...] のリスト
        """
        results = []
        codecs_to_try = self._get_available_codecs()

        for codec in codecs_to_try:
            try:
                decoded = byte_data.decode(codec)
                results.append((codec, decoded))
            except (UnicodeDecodeError, LookupError):
                pass

        return results

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
