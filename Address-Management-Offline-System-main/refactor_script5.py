import sys

with open('ui/address_view.py', 'r', encoding='utf-8') as f:
    content = f.read()

zoomable_class = """
class ZoomableTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.viewport().setCursor(Qt.OpenHandCursor)
        self._is_panning = False
        self._pan_start_x = 0
        self._pan_start_y = 0
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoomIn(1)
            else:
                self.zoomOut(1)
        else:
            super().wheelEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_panning = True
            self._pan_start_x = int(event.position().x())
            self._pan_start_y = int(event.position().y())
            self.viewport().setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._is_panning:
            dx = int(event.position().x()) - self._pan_start_x
            dy = int(event.position().y()) - self._pan_start_y
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - dx)
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - dy)
            self._pan_start_x = int(event.position().x())
            self._pan_start_y = int(event.position().y())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_panning = False
            self.viewport().setCursor(Qt.OpenHandCursor)
        super().mouseReleaseEvent(event)
"""

if "class ZoomableTextEdit" not in content:
    # Add ZoomableTextEdit right before AddressView class
    content = content.replace("class AddressView(QWidget):", zoomable_class + "\nclass AddressView(QWidget):")

# Replace preview_text = QTextEdit() with ZoomableTextEdit() inside _open_envelope_preview_dialog
target_preview = """        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        preview_text = QTextEdit()
        preview_text.setReadOnly(True)"""

replacement_preview = """        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Action row for Zoom controls
        toolbar_row = QHBoxLayout()
        zoom_in_btn = QPushButton("🔍 Zoom In")
        zoom_in_btn.clicked.connect(lambda: preview_text.zoomIn(1))
        zoom_out_btn = QPushButton("🔍 Zoom Out")
        zoom_out_btn.clicked.connect(lambda: preview_text.zoomOut(1))
        
        toolbar_row.addWidget(zoom_in_btn)
        toolbar_row.addWidget(zoom_out_btn)
        toolbar_row.addStretch()
        layout.addLayout(toolbar_row)
        
        preview_text = ZoomableTextEdit()
        preview_text.setReadOnly(True)"""

if target_preview in content:
    content = content.replace(target_preview, replacement_preview)
    with open('ui/address_view.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Success")
else:
    print("Target preview not found")
