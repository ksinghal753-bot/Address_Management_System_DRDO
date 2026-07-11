import sys

with open('ui/address_view.py', 'r', encoding='utf-8') as f:
    content = f.read()

target_class = """class ZoomableTextEdit(QTextEdit):
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
        super().mouseReleaseEvent(event)"""

zoomable_class = """from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PySide6.QtGui import QBrush, QPen, QColor, QTextDocument
from PySide6.QtCore import QSizeF

class ZoomablePreview(QGraphicsView):
    def __init__(self, html, parent=None):
        super().__init__(parent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.text_doc = QTextDocument()
        self.text_doc.setHtml(html)
        
        # A4 Landscape: 1123 x 794
        width = 1123
        height = 794
        
        self.bg_rect = QGraphicsRectItem(0, 0, width, height)
        self.bg_rect.setBrush(QBrush(QColor("white")))
        self.bg_rect.setPen(QPen(QColor("#999999")))
        
        self.doc_item = QGraphicsTextItem()
        self.doc_item.setDocument(self.text_doc)
        
        # Add padding
        padding = 40
        self.text_doc.setTextWidth(width - padding * 2)
        self.doc_item.setPos(padding, padding)
        
        self.scene.addItem(self.bg_rect)
        self.scene.addItem(self.doc_item)
        
        self.setBackgroundBrush(QBrush(QColor("#FAFAFA")))

        # Fit in view initially, slightly scaled down
        self.scale(0.7, 0.7)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoomIn()
            else:
                self.zoomOut()
        else:
            super().wheelEvent(event)
            
    def zoomIn(self):
        self.scale(1.2, 1.2)
        
    def zoomOut(self):
        self.scale(1 / 1.2, 1 / 1.2)"""

content = content.replace(target_class, zoomable_class)

target_preview = """        preview_text = ZoomableTextEdit()
        preview_text.setReadOnly(True)
        preview_text.setHtml(html)
        
        preview_text.setStyleSheet(\"\"\"
            QTextEdit {
                background-color: #FAFAFA;
                color: #000000;
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                padding: 20px;
            }
        \"\"\")"""

replacement_preview = """        preview_text = ZoomablePreview(html)
        preview_text.setStyleSheet(\"\"\"
            QGraphicsView {
                border: 1px solid #CCCCCC;
                border-radius: 8px;
            }
        \"\"\")"""

if target_preview in content:
    content = content.replace(target_preview, replacement_preview)
    with open('ui/address_view.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Success")
else:
    print("Target preview not found")
