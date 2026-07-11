from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QFrame
from PySide6.QtCore import Qt

class ExportFormatDialog(QDialog):
    def __init__(self, parent=None, allow_excel: bool = True):
        super().__init__(parent)
        self.setWindowTitle("Print / Export Options")
        self.setFixedSize(400, 300)
        self.selected_option = None  # Will be "pdf", "excel", or "direct"

        self._build_ui(allow_excel)

    def _build_ui(self, allow_excel: bool):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel("Choose Output Format")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333333; margin-bottom: 10px;")
        layout.addWidget(header)

        # Line separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #DDDDDD;")
        layout.addWidget(line)

        btn_style = """
            QPushButton {
                font-size: 13pt;
                font-weight: bold;
                padding: 12px;
                border-radius: 6px;
                background-color: #F8F9FA;
                border: 1px solid #CCCCCC;
                color: #333333;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #E2E6EA;
                border: 1px solid #adb5bd;
            }
            QPushButton:disabled {
                background-color: #F8F9FA;
                color: #AAAAAA;
            }
        """

        # Option 1: PDF
        self.btn_pdf = QPushButton("📄 Export as PDF")
        self.btn_pdf.setStyleSheet(btn_style)
        self.btn_pdf.setCursor(Qt.PointingHandCursor)
        self.btn_pdf.clicked.connect(lambda: self._select("pdf"))
        layout.addWidget(self.btn_pdf)

        # Option 2: Excel
        self.btn_excel = QPushButton("📊 Export as Excel")
        self.btn_excel.setStyleSheet(btn_style)
        if not allow_excel:
            self.btn_excel.setEnabled(False)
            self.btn_excel.setToolTip("Excel export is available only for list-based reports, not label layouts.")
        else:
            self.btn_excel.setCursor(Qt.PointingHandCursor)
            self.btn_excel.clicked.connect(lambda: self._select("excel"))
        layout.addWidget(self.btn_excel)

        # Option 3: Direct Print
        self.btn_direct = QPushButton("🖨 Print Directly")
        self.btn_direct.setStyleSheet(btn_style)
        self.btn_direct.setCursor(Qt.PointingHandCursor)
        self.btn_direct.clicked.connect(lambda: self._select("direct"))
        layout.addWidget(self.btn_direct)

        layout.addStretch()

        # Cancel button
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #EEEEEE;
                color: #333;
                border-radius: 4px;
                padding: 8px;
                font-size: 11pt;
            }
            QPushButton:hover { background-color: #DDDDDD; }
        """)
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.clicked.connect(self.reject)
        
        cancel_layout = QHBoxLayout()
        cancel_layout.addStretch()
        cancel_layout.addWidget(self.btn_cancel)
        cancel_layout.addStretch()
        layout.addLayout(cancel_layout)

    def _select(self, option: str):
        self.selected_option = option
        self.accept()
