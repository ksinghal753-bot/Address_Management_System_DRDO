import sys
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PySide6.QtGui import QBrush, QPen, QColor, Qt, QTextDocument, QFont
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
        
        self.setBackgroundBrush(QBrush(QColor("#E0E0E0")))
        self.scale(0.7, 0.7)

html = """
        <html>
        <body style="margin: 0; padding: 0;">
          <table width="100%" style="border-collapse: collapse; margin-bottom: 5px;">
            <tr>
              <td align="left" style="font-family: 'Courier New', monospace; font-size: 14pt; font-weight: bold; color: #1a237e; border: none; padding: 0;">NO.:- ADRDE/AS-QMS/PARA1</td>
              <td align="right" style="font-family: 'Courier New', monospace; font-size: 14pt; font-weight: bold; color: #1a237e; border: none; padding: 0;">By S/P:- Ordinary/साधारण</td>
            </tr>
          </table>
          <div style="font-family: 'Courier New', monospace; font-size: 14pt; font-weight: bold; color: #1a237e; margin-bottom: 60px;">Date:- 23-06-2026</div>
          
          <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>
              <td align="center">
                <table border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td align="left">
                        <div style="font-family: 'Courier New', monospace; font-size: 14pt; color: #000000; line-height: 1.5;">To,</div>
                        <div style="font-family: 'Courier New', monospace; font-size: 14pt; color: #000000; line-height: 1.5;">&nbsp;&nbsp;&nbsp;&nbsp;Director</div>
                        <div style="font-family: 'Courier New', monospace; font-size: 14pt; color: #000000; line-height: 1.5;">&nbsp;&nbsp;&nbsp;&nbsp;ADRDE</div>
                        <div style="font-family: 'Courier New', monospace; font-size: 14pt; color: #000000; line-height: 1.5;">&nbsp;&nbsp;&nbsp;&nbsp;PB No. 51</div>
                        <div style="font-family: 'Courier New', monospace; font-size: 14pt; color: #000000; line-height: 1.5;">&nbsp;&nbsp;&nbsp;&nbsp;Agra Cantt, UP</div>
                        <div style="font-family: 'Courier New', monospace; font-size: 14pt; color: #000000; line-height: 1.5;">&nbsp;&nbsp;&nbsp;&nbsp;PIN Code: 282001</div>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </body>
        </html>
"""

app = QApplication(sys.argv)
w = QWidget()
l = QVBoxLayout(w)
preview = ZoomablePreview(html)
l.addWidget(preview)
w.resize(900, 600)
w.show()
sys.exit(app.exec())
