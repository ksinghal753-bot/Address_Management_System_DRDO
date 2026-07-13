"""
Address View / Search / Print Screen.
Available to both Admin (with edit/delete) and User (view/print only).
"""

import os
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QListView, QCalendarWidget, QStyleFactory, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QGroupBox, QSplitter, QTextEdit, QFrame,
    QAbstractItemView, QFileDialog, QSizePolicy, QCheckBox, QGridLayout, QDialog, QDialogButtonBox, QScrollArea, QRadioButton, QFormLayout
)
from PySide6.QtCore import Qt, Signal, QDate, QSize
from PySide6.QtGui import QFont, QColor

from modules.address_ops import (
    get_all_addresses, search_addresses, delete_address, get_address_stats
)
from modules.department_ops import get_all_departments
from modules.print_module import (
    generate_single_envelope_pdf, generate_department_list_pdf,
    generate_full_directory_pdf, generate_multiple_envelopes_pdf,
    generate_single_label_pdf, generate_multiple_labels_pdf, open_pdf,
    get_default_output_dir, format_ref_no
)
from ui.shared_widgets import (
    HeaderBar, SectionTitle, HLine, show_error, show_info,
    show_warning, show_question
)
from utils.constants import COLORS, LABELS, PARA_OPTIONS, DELIVERY_TYPES, ENVELOPE_PREFIX

def wrap_text_html_fonts(text: str) -> str:
    """Wrap Hindi/Devanagari text in a span using 'Mangal' font and English/numbers in 'Arial' font."""
    if not text:
        return ""
    text = str(text)
    import html
    escaped = html.escape(text)
    
    import re
    parts = re.split(r'([\u0900-\u097F]+)', escaped)
    result = []
    for part in parts:
        if not part:
            continue
        if any('\u0900' <= char <= '\u097F' for char in part):
            result.append(f'<span style="font-family: Mangal;">{part}</span>')
        else:
            result.append(f'<span style="font-family: Arial;">{part}</span>')
    return "".join(result)


TABLE_COLUMNS = [
    ("ID", "id"),
    ("Select / चुनें", "select"),
    ("Actions / क्रिया", "actions"),
    ("Dept / विभाग", "dept_name"),
    ("Designation / पदनाम", "designation"),
    ("Office / कार्यालय", "office_name"),
    ("City / शहर", "city"),
    ("State / राज्य", "state"),
    ("PIN", "pin_code"),
    ("Email / ईमेल", "email"),
    ("Contact / संपर्क", "contact_no"),
    ("Fax / फैक्स", "fax"),
    ("Print", "print_action"),
    ("Open", "open_action"),
    ("Edit", "edit_action"),
]



class ColumnSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Columns / कॉलम चुनें")
        self.resize(320, 450)
        self.setStyleSheet(f"QDialog {{ background-color: {COLORS['surface']}; }}")
        
        layout = QVBoxLayout(self)
        
        title = QLabel("Select Columns to Print")
        title.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {COLORS['primary']};")
        layout.addWidget(title)
        
        self.checkboxes = {}
        
        self.columns = [
            ("dept_name", "Dept / विभाग"),
            ("to_field", "To / सेवा में"),
            ("designation", "Designation / पदनाम"),
            ("office_name", "Office Name / कार्यालय"),
            ("address", "Address / पता"),
            ("city_state", "City, State / शहर, राज्य"),
            ("pin_code", "PIN / पिन"),
            ("email", "Email / ईमेल"),
            ("contact_no", "Contact / संपर्क"),
            ("fax", "Fax / फैक्स"),
            ("para_no", "PARA / पैरा"),
            ("date_entry", "Date / दिनांक"),
            ("delivery_type", "By S/P / डाक")
        ]
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: 1px solid #ddd; background-color: #fff;")
        
        inner_widget = QWidget()
        inner_layout = QVBoxLayout(inner_widget)
        
        for key, label in self.columns:
            cb = QCheckBox(label)
            cb.setChecked(True)
            cb.setStyleSheet("font-size: 12px; padding: 2px;")
            self.checkboxes[key] = cb
            inner_layout.addWidget(cb)
            
        inner_layout.addStretch(1)
        scroll.setWidget(inner_widget)
        layout.addWidget(scroll, stretch=1)
        
        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("Print / प्रिंट")
        self.btn_ok.setStyleSheet("background-color: #7A1212; color: #fff; font-weight: bold; padding: 6px; border-radius: 4px;")
        self.btn_ok.clicked.connect(self.accept)
        
        self.btn_cancel = QPushButton("Cancel / रद्द करें")
        self.btn_cancel.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; padding: 6px; border-radius: 4px;")
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)
        
    def get_selected_columns(self):
        return [key for key, label in self.columns if self.checkboxes[key].isChecked()]


class EnvelopeReferenceDialog(QDialog):
    def __init__(self, parent=None, records: list[dict] = None):
        super().__init__(parent)
        self.records = records or []
        self.setWindowTitle("Envelope Reference / लिफाफा संदर्भ")
        
        num_recs = len(self.records)
        height = min(650, 200 + num_recs * 220)
        self.resize(600, height)
        self.setStyleSheet(f"QDialog {{ background-color: {COLORS['surface']}; }}")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        title = QLabel(f"Envelope Reference Details ({num_recs} Addresses) / लिफाफा संदर्भ विवरण")
        title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {COLORS['primary']}; margin-bottom: 8px;")
        layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 10, 0)
        scroll_layout.setSpacing(16)
        
        self.record_inputs = []
        
        for idx, rec in enumerate(self.records):
            group = QGroupBox(f"Address {idx + 1}: {rec.get('office_name', '')} ({rec.get('city', '')})")
            group.setStyleSheet(
                f"QGroupBox {{"
                f"  font-weight: bold;"
                f"  color: {COLORS['primary']};"
                f"  border: 1.5px solid {COLORS['border']};"
                f"  border-radius: 8px;"
                f"  margin-top: 12px;"
                f"  padding-top: 12px;"
                f"}}"
                f"QGroupBox::title {{"
                f"  subcontrol-origin: margin;"
                f"  left: 10px;"
                f"  padding: 0 5px;"
                f"}}"
            )
            
            group_layout = QFormLayout(group)
            group_layout.setSpacing(10)
            group_layout.setContentsMargins(12, 16, 12, 12)
            
            date_edit = QDateEdit()
            cal = QCalendarWidget()
            cal.setStyleSheet("""
    QCalendarWidget { 
        background-color: #FFFFFF; 
        color: #1E293B;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
    }
    QCalendarWidget QWidget {
        background-color: #FFFFFF;
        alternate-background-color: #F8FAFC;
    }
    QCalendarWidget QWidget#qt_calendar_navigationbar { 
        background-color: #FFFFFF; 
        border-bottom: 1px solid #E5E7EB; 
    }
    QCalendarWidget QToolButton { 
        color: #1E293B; 
        background-color: transparent; 
        font-weight: bold; 
    }
    QCalendarWidget QToolButton:hover { background-color: #EFF6FF; }
    QCalendarWidget QSpinBox { background-color: #FFFFFF; color: #1E293B; }
    QCalendarWidget QTableView { 
        background-color: #FFFFFF; 
        alternate-background-color: #F8FAFC;
        color: #1E293B; 
        selection-background-color: #2563EB; 
        selection-color: #FFFFFF;
        border: none;
    }
    QCalendarWidget QTableView::item {
        background-color: #FFFFFF;
        color: #1E293B;
    }
    QCalendarWidget QTableView::item:selected {
        background-color: #2563EB;
        color: #FFFFFF;
    }
    QCalendarWidget QAbstractItemView:enabled {
        color: #1E293B;
        background-color: #FFFFFF;
        selection-background-color: #2563EB;
        selection-color: #FFFFFF;
    }
    QCalendarWidget QAbstractItemView:disabled {
        color: #94A3B8;
    }
    QCalendarWidget QHeaderView { background-color: #FFFFFF; border: none; }
    QCalendarWidget QHeaderView::section { 
        background-color: #FFFFFF; 
        color: #1E293B; 
        font-weight: bold; 
    }
    QMenu {
        background-color: #FFFFFF;
        color: #333333;
        border: 1px solid #E5E7EB;
    }
    QMenu::item {
        background-color: transparent;
        color: #333333;
        padding: 4px 16px;
    }
    QMenu::item:selected {
        background-color: #E3F2FD;
    }
    QListView {
        background-color: #FFFFFF;
        color: #333333;
    }

""")
            cal.setStyle(QStyleFactory.create('Fusion'))
            palette = cal.palette()
            from PySide6.QtGui import QColor, QPalette
            palette.setColor(QPalette.Window, QColor(255, 255, 255))
            palette.setColor(QPalette.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.Text, QColor(0, 0, 0))
            palette.setColor(QPalette.Button, QColor(255, 255, 255))
            palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
            cal.setPalette(palette)
            from PySide6.QtGui import QTextCharFormat, QColor
            from PySide6.QtCore import Qt
            fmt = QTextCharFormat()
            fmt.setForeground(QColor('#E53935'))
            cal.setWeekdayTextFormat(Qt.Sunday, fmt)
            date_edit.setCalendarWidget(cal)
            date_edit.setCalendarPopup(True)
            date_edit.setDisplayFormat("dd-MM-yyyy")
            date_edit.setMinimumHeight(34)
            rec_date = QDate.currentDate()
            if rec.get("date_entry"):
                try:
                    dt = datetime.strptime(rec["date_entry"], "%Y-%m-%d")
                    rec_date = QDate(dt.year, dt.month, dt.day)
                except Exception:
                    pass
            date_edit.setDate(rec_date)
            
            para_combo = QComboBox()
            para_combo.setStyle(QStyleFactory.create('Fusion'))
            para_combo.setView(QListView())
            para_combo.addItems(PARA_OPTIONS)
            para_combo.setMinimumHeight(34)
            if rec.get("para_no"):
                c_idx = para_combo.findText(rec["para_no"])
                if c_idx >= 0:
                    para_combo.setCurrentIndex(c_idx)
                    
            suffix_edit = QLineEdit()
            suffix_edit.setPlaceholderText("Write suffix here...")
            suffix_edit.setMinimumHeight(34)
            if rec.get("ref_suffix"):
                suffix_edit.setText(rec["ref_suffix"])
                
            sp_combo = QComboBox()
            sp_combo.setStyle(QStyleFactory.create('Fusion'))
            sp_combo.setView(QListView())
            sp_combo.addItems(DELIVERY_TYPES)
            sp_combo.setMinimumHeight(34)
            if rec.get("delivery_type"):
                c_idx = sp_combo.findText(rec["delivery_type"])
                if c_idx >= 0:
                    sp_combo.setCurrentIndex(c_idx)
                    
            def make_lbl(text):
                lbl = QLabel(text)
                lbl.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {COLORS['text_primary']};")
                return lbl
                
            group_layout.addRow(make_lbl("Date / दिनांक *"), date_edit)
            group_layout.addRow(make_lbl("PARA No. / पैरा नं. *"), para_combo)
            group_layout.addRow(make_lbl("Custom Text / अतिरिक्त पाठ"), suffix_edit)
            group_layout.addRow(make_lbl("By S/P / डाक प्रकार"), sp_combo)
            
            scroll_layout.addWidget(group)
            
            self.record_inputs.append({
                "date_edit": date_edit,
                "para_combo": para_combo,
                "suffix_edit": suffix_edit,
                "sp_combo": sp_combo
            })
            
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll, stretch=1)
        
        button_box = QHBoxLayout()
        button_box.addStretch()
        
        self.btn_cancel = QPushButton("Cancel / रद्द करें")
        self.btn_cancel.setMinimumHeight(38)
        self.btn_cancel.setStyleSheet(
            "QPushButton {"
            "  background-color: #FAFAFA;"
            "  color: #333333;"
            "  border: 1.5px solid #CCCCCC;"
            "  border-radius: 6px;"
            "  font-size: 13px;"
            "  font-weight: bold;"
            "  padding: 0 16px;"
            "}"
            "QPushButton:hover {"
            "  background-color: #EEEEEE;"
            "}"
        )
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_save = QPushButton("💾 Save / सहेजें")
        self.btn_save.setMinimumHeight(38)
        self.btn_save.setStyleSheet(
            "QPushButton {"
            "  background-color: #1f6b2e;"
            "  color: #FFFFFF;"
            "  border: none;"
            "  border-radius: 6px;"
            "  font-size: 13px;"
            "  font-weight: bold;"
            "  padding: 0 16px;"
            "}"
            "QPushButton:hover {"
            "  background-color: #154c20;"
            "}"
        )
        self.btn_save.clicked.connect(lambda: self.done_with_action("save"))
        
        self.btn_ok = QPushButton("🖨️ Proceed to Print")
        self.btn_ok.setMinimumHeight(38)
        self.btn_ok.setStyleSheet(
            "QPushButton {"
            "  background-color: #7A1212;"
            "  color: #FFFFFF;"
            "  border: none;"
            "  border-radius: 6px;"
            "  font-size: 13px;"
            "  font-weight: bold;"
            "  padding: 0 16px;"
            "}"
            "QPushButton:hover {"
            "  background-color: #5C0D0D;"
            "}"
        )
        self.btn_ok.clicked.connect(lambda: self.done_with_action("print"))
        
        button_box.addWidget(self.btn_cancel)
        button_box.addWidget(self.btn_save)
        button_box.addWidget(self.btn_ok)
        layout.addLayout(button_box)
        
        self.selected_action = "print"

    def done_with_action(self, action):
        self.selected_action = action
        self.accept()

    def get_selected_action(self) -> str:
        return getattr(self, "selected_action", "print")

    def get_values_list(self) -> list[dict]:
        results = []
        for i, inputs in enumerate(self.record_inputs):
            results.append({
                "date_entry": inputs["date_edit"].date().toString("yyyy-MM-dd"),
                "para_no": inputs["para_combo"].currentText(),
                "ref_suffix": inputs["suffix_edit"].text().strip(),
                "delivery_type": inputs["sp_combo"].currentText()
            })
        return results


class PrintOptionsDialog(QDialog):
    def __init__(self, parent=None, has_selected=False, has_checked=False, has_dept=False):
        super().__init__(parent)
        self.setWindowTitle("Print Options / प्रिंट विकल्प")
        self.resize(450, 275)
        self.setStyleSheet(f"QDialog {{ background-color: {COLORS['surface']}; }}")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)
        
        title = QLabel("Select Print Option / प्रिंट विकल्प चुनें")
        title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {COLORS['primary']}; margin-bottom: 8px;")
        layout.addWidget(title)
        
        def create_btn(text, is_primary, enabled):
            btn = QPushButton(text)
            btn.setMinimumHeight(44)
            btn.setEnabled(enabled)
            btn.setCursor(Qt.PointingHandCursor if enabled else Qt.ArrowCursor)
            
            if is_primary:
                if enabled:
                    btn.setStyleSheet(
                        "QPushButton {"
                        "  background-color: #7A1212;"
                        "  color: #FFFFFF;"
                        "  border: 1px solid #7A1212;"
                        "  border-radius: 6px;"
                        "  font-size: 13px;"
                        "  font-weight: bold;"
                        "}"
                        "QPushButton:hover {"
                        "  background-color: #5C0D0D;"
                        "}"
                    )
                else:
                    btn.setStyleSheet(
                        "QPushButton {"
                        "  background-color: #E0E0E0;"
                        "  color: #757575;"
                        "  border: 1px solid #BDBDBD;"
                        "  border-radius: 6px;"
                        "  font-size: 13px;"
                        "  font-weight: bold;"
                        "}"
                    )
            else:
                if enabled:
                    btn.setStyleSheet(
                        "QPushButton {"
                        "  background-color: #FAFAFA;"
                        "  color: #7A1212;"
                        "  border: 1.5px solid #7A1212;"
                        "  border-radius: 6px;"
                        "  font-size: 13px;"
                        "  font-weight: bold;"
                        "}"
                        "QPushButton:hover {"
                        "  background-color: #F0F0F0;"
                        "}"
                    )
                else:
                    btn.setStyleSheet(
                        "QPushButton {"
                        "  background-color: #EEEEEE;"
                        "  color: #9E9E9E;"
                        "  border: 1.5px solid #D0D0D0;"
                        "  border-radius: 6px;"
                        "  font-size: 13px;"
                        "  font-weight: bold;"
                        "}"
                    )
            return btn
            
        self.btn_envelope = create_btn("✉️ Print Selected envelopes / चयनित लिफाफे प्रिंट करें", True, has_selected or has_checked)
        self.btn_dept = create_btn("📋 Print Department List / विभाग सूची", False, True)
        self.btn_all = create_btn("📄 Print Full Directory (All) / सभी पते", False, True)
        
        self.btn_cancel = QPushButton("Cancel / रद्द करें")
        self.btn_cancel.setMinimumHeight(40)
        self.btn_cancel.setStyleSheet(
            "QPushButton {"
            "  background-color: #FAFAFA;"
            "  color: #333333;"
            "  border: 1.5px solid #CCCCCC;"
            "  border-radius: 6px;"
            "  font-size: 13px;"
            "  font-weight: bold;"
            "}"
            "QPushButton:hover {"
            "  background-color: #EEEEEE;"
            "}"
        )
        self.btn_cancel.clicked.connect(self.reject)
        
        layout.addWidget(self.btn_envelope)
        layout.addWidget(self.btn_dept)
        layout.addWidget(self.btn_all)
        layout.addWidget(self.btn_cancel)
        
        self.selected_option = None
        self.btn_envelope.clicked.connect(lambda: self.done_with_option("envelope"))
        self.btn_dept.clicked.connect(lambda: self.done_with_option("dept"))
        self.btn_all.clicked.connect(lambda: self.done_with_option("all"))
        
    def done_with_option(self, option):
        self.selected_option = option
        self.accept()



from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PySide6.QtGui import QBrush, QPen, QColor, QTextDocument
from PySide6.QtCore import QSizeF

class ZoomablePreview(QGraphicsView):
    def __init__(self, html, parent=None, paper_size="a4"):
        super().__init__(parent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        if isinstance(html, str):
            html_list = [html]
        else:
            html_list = html
            
        if paper_size == "envelope":
            # DL Envelope (220 x 110 mm) at 96 DPI: ~831 x 416
            width = 831
            height = 416
        else:
            # A4 Landscape: 1123 x 794
            width = 1123
            height = 794
            
        padding = 40
        gap = 20
        y_offset = 0
        
        # Render each envelope visually
        for h in html_list:
            bg_rect = QGraphicsRectItem(0, y_offset, width, height)
            bg_rect.setBrush(QBrush(QColor("white")))
            pen = QPen(QColor("#777777"))
            pen.setWidth(2)
            bg_rect.setPen(pen)
            self.scene.addItem(bg_rect)
            
            doc = QTextDocument()
            doc.setPageSize(QSizeF(width, height))
            doc.setHtml(h)
            doc.setTextWidth(width - padding * 2)
            
            doc_item = QGraphicsTextItem()
            doc_item.setDocument(doc)
            doc_item.setPos(padding, y_offset + padding)
            self.scene.addItem(doc_item)
            
            y_offset += height + gap
            
        # Create a combined document strictly for the QPrinter to use
        self.text_doc = QTextDocument()
        self.text_doc.setPageSize(QSizeF(width, height))
        self.text_doc.setTextWidth(width - padding * 2)
        
        from PySide6.QtGui import QTextCursor, QTextBlockFormat, QTextFormat
        cursor = QTextCursor(self.text_doc)
        
        for i, h in enumerate(html_list):
            if i > 0:
                block_fmt = QTextBlockFormat()
                block_fmt.setPageBreakPolicy(QTextFormat.PageBreak_AlwaysBefore)
                cursor.insertBlock(block_fmt)
            cursor.insertHtml(h)
        
        self.setBackgroundBrush(QBrush(QColor("#E0E0E0"))) # Darker background to highlight white envelopes

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
        self.scale(1 / 1.2, 1 / 1.2)

class ReferenceLabelPreviewDialog(QDialog):
    def __init__(self, parent, records):
        super().__init__(parent)
        self.records = records
        self.selected_print_mode = "both"
        self.setWindowTitle("Preview Reference Label(s) / संदर्भ लेबल पूर्वावलोकन")
        self.setMinimumSize(650, 500)
        
        layout = QVBoxLayout(self)
        
        # Info Label
        info = QLabel(f"Previewing {len(records)} label(s). NO: and Date: auto-populated from record data.")
        info.setStyleSheet("color: #444; font-size: 13px; font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(info)
        
        # Print Options Group
        mode_group = QGroupBox("Print Layout Option")
        mode_group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #CCC; border-radius: 4px; margin-top: 10px; padding-top: 15px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }")
        mode_layout = QHBoxLayout()
        self.rb_both = QRadioButton("Print Both Sides")
        self.rb_left = QRadioButton("Print Left Only (NO/Date)")
        self.rb_right = QRadioButton("Print Right Only (Address)")
        self.rb_both.setChecked(True)
        
        self.rb_both.toggled.connect(self._update_preview)
        self.rb_left.toggled.connect(self._update_preview)
        self.rb_right.toggled.connect(self._update_preview)
        
        mode_layout.addWidget(self.rb_both)
        mode_layout.addWidget(self.rb_left)
        mode_layout.addWidget(self.rb_right)
        mode_layout.addStretch()
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)
        
        # Preview Text Area
        self.preview_area = QTextEdit()
        self.preview_area.setReadOnly(True)
        self.preview_area.setStyleSheet("background-color: #FAFAFA; border: 1px solid #CCC; font-size: 14px; padding: 10px;")
        layout.addWidget(self.preview_area, stretch=1)
        
        self._update_preview()
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_print = QPushButton("🖨 Print")
        self.btn_print.setStyleSheet("QPushButton { background-color: #7A1212; color: white; border-radius: 4px; padding: 8px 16px; font-weight: bold; } QPushButton:hover { background-color: #5C0D0D; }")
        self.btn_print.clicked.connect(self.accept)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_print)
        layout.addLayout(btn_layout)

    def _update_preview(self):
        if self.rb_both.isChecked():
            self.selected_print_mode = "both"
        elif self.rb_left.isChecked():
            self.selected_print_mode = "left"
        elif self.rb_right.isChecked():
            self.selected_print_mode = "right"
            
        html = "<html><body style='font-family: sans-serif;'>"
        from modules.print_module import format_ref_no
        for rec in self.records:
            ref_str = format_ref_no(rec.get("para_no", ""), rec.get("date_entry", ""), rec.get("ref_suffix", ""))
            ref_parts = ref_str.split("\n")
            no_line = ref_parts[0] if len(ref_parts) > 0 else "NO: -"
            date_line = ref_parts[1].replace("Date:- ", "Date:-") if len(ref_parts) > 1 else "Date: -"
            
            html += "<table width='100%' style='border: 1px dashed #888; margin-bottom: 15px; border-collapse: collapse;'>"
            html += "<tr>"
            
            left_html = f"<div style='margin-bottom: 25px;'><strong>{no_line}</strong></div>"
            left_html += f"<div><strong>{date_line}</strong></div>"
            
            right_html = "<strong>TO,</strong><br>"
            indent_html = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
            if rec.get("to_field"):
                right_html += f"{indent_html}{rec['to_field']}<br>"
            if rec.get("designation"):
                right_html += f"{indent_html}{rec['designation']}<br>"
            if rec.get("office_name"):
                right_html += f"{indent_html}{rec['office_name']}<br>"
            if rec.get("addr_line1"):
                right_html += f"{indent_html}{rec['addr_line1']}<br>"
            if rec.get("addr_line2"):
                right_html += f"{indent_html}{rec['addr_line2']}<br>"
                
            city_state_pin = ", ".join(filter(None, [rec.get("city", ""), rec.get("state", "")]))
            if rec.get("pin_code"):
                if city_state_pin:
                    city_state_pin += " - " + rec["pin_code"]
                else:
                    city_state_pin = "PIN: " + rec["pin_code"]
            if city_state_pin:
                right_html += f"{indent_html}{city_state_pin}<br>"
            
            if self.selected_print_mode == "both":
                html += f"<td width='50%' style='padding: 15px; vertical-align: top; border-right: 1px solid #333;'>{left_html}</td>"
                html += f"<td width='50%' style='padding: 15px; padding-left: 30px; vertical-align: top;'>{right_html}</td>"
            elif self.selected_print_mode == "left":
                html += f"<td width='100%' style='padding: 15px; vertical-align: top;'>{left_html}</td>"
            elif self.selected_print_mode == "right":
                html += f"<td width='100%' style='padding: 15px; vertical-align: top;'>{right_html}</td>"
            
            html += "</tr>"
            html += "</table>"
            
        html += "</body></html>"
        self.preview_area.setHtml(html)

class AddressView(QWidget):
    """
    Combined search + table + envelope preview + print panel.
    role: 'admin' | 'user'
    Emits: go_back(), edit_record(dict), add_new()
    """
    go_back     = Signal()
    edit_record = Signal(dict)
    add_new     = Signal()

    def __init__(self, role: str = "user", mode: str = "view", parent=None):
        super().__init__(parent)
        self.role = role
        self.mode = mode
        self._records: list[dict] = []
        self._selected_record: dict | None = None
        self._build_ui()
        self._load_records()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)



        # ── Toolbar ───────────────────────────────────────────────────────────
        toolbar = QWidget()
        toolbar.setStyleSheet(f"background: {COLORS['primary_dark']}; padding: 4px 12px;")
        tl = QHBoxLayout(toolbar)
        tl.setContentsMargins(10, 6, 10, 6)
        tl.setSpacing(10)

        title_text = "📋  Address Records / पता अभिलेख"
        if self.mode == "search":
            title_text = "🔍  Search Address / पता खोजें"
        elif self.mode == "edit":
            title_text = "✏️  Edit Address / पता संपादित करें"
        elif self.mode == "delete":
            title_text = "🗑️  Delete Address / पता हटाएं"
            
        title = QLabel(title_text)
        title.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        tl.addWidget(title)
        tl.addStretch()

        # Stats label
        self.stats_lbl = QLabel("")
        self.stats_lbl.setStyleSheet(f"color: {COLORS['accent_light']}; font-size: 12px;")
        tl.addWidget(self.stats_lbl)

        back_btn = QPushButton("← " + LABELS["return"])
        back_btn.clicked.connect(self.go_back.emit)
        tl.addWidget(back_btn)

        root.addWidget(toolbar)

        # ── Top Splitter (Search / Preview) ───────────────────────────────────
        top_layout = QHBoxLayout()
        # Set only 12px vertical gap under the toolbar
        top_layout.setContentsMargins(12, 12, 12, 0)
        top_layout.setSpacing(12)

        # Left: Search panel (Using QWidget instead of QGroupBox to remove large white space)
        search_widget = QWidget()
        search_widget.setObjectName("addressViewSearch")
        search_widget.setStyleSheet(f"#addressViewSearch {{ background-color: {COLORS['surface']}; border: 1.5px solid {COLORS['border']}; border-radius: 12px; }}")
        search_vbox = QVBoxLayout(search_widget)
        search_vbox.setContentsMargins(12, 12, 12, 12)
        search_vbox.setSpacing(8)

        # Left header removed by request

        # Reverting to the 1st screenshot layout (Grid of 6 buttons)
        grid = QGridLayout()
        grid.setSpacing(6)
        
        self.add_btn = QPushButton("➕ Add Address")
        self.add_btn.setStyleSheet("background-color: #1f6b2e; color: white; border-radius: 6px; padding: 8px; font-weight: bold;")
        self.add_btn.clicked.connect(self.add_new.emit)
        
        self.edit_btn = QPushButton("✏️ Edit Address")
        self.edit_btn.setObjectName("secondaryButton")
        self.edit_btn.clicked.connect(self._edit_selected)
        self.edit_btn.setEnabled(False)

        self.del_btn = QPushButton("🗑️ Delete")
        self.del_btn.setObjectName("secondaryButton")
        self.del_btn.clicked.connect(self._delete_selected)
        self.del_btn.setEnabled(False)

        self.view_btn = QPushButton("👁️ View")
        self.view_btn.setObjectName("secondaryButton")
        self.view_btn.clicked.connect(self._view_selected)
        self.view_btn.setEnabled(False)

        self.clear_sel_btn = QPushButton("🧹 Clear")
        self.clear_sel_btn.setObjectName("secondaryButton")
        self.clear_sel_btn.clicked.connect(self._clear_search)
        self.clear_sel_btn.clicked.connect(self._clear_selection)

        self.print_btn = QPushButton("🖨️ Print")
        self.print_btn.setStyleSheet("background-color: #8B0000; color: white; border-radius: 6px; padding: 8px; font-weight: bold;")
        # Note: using the same action as the old print_btn. If _show_print_dialog doesn't exist, we fallback.
        if hasattr(self, '_show_print_dialog'):
            self.print_btn.clicked.connect(self._show_print_dialog)
        else:
            self.print_btn.clicked.connect(self._print_single)

        grid.addWidget(self.add_btn, 0, 0)
        grid.addWidget(self.edit_btn, 0, 1)
        grid.addWidget(self.view_btn, 0, 2)
        grid.addWidget(self.clear_sel_btn, 0, 3)
        grid.addWidget(self.del_btn, 0, 4)
        grid.addWidget(self.print_btn, 0, 5)

        search_vbox.addLayout(grid)
        search_vbox.addWidget(HLine())

        row1 = QHBoxLayout()
        row1.setSpacing(6)
        
        dept_lbl = QLabel("Dept:")
        dept_lbl.setObjectName("fieldLabel")
        self.dept_filter = QComboBox()
        self.dept_filter.setStyle(QStyleFactory.create('Fusion'))
        self.dept_filter.setView(QListView())
        self.dept_filter.setMinimumWidth(120)
        self._load_dept_filter()

        para_lbl = QLabel("PARA:")
        para_lbl.setObjectName("fieldLabel")
        self.para_filter = QComboBox()
        self.para_filter.setStyle(QStyleFactory.create('Fusion'))
        self.para_filter.setView(QListView())
        self.para_filter.setMinimumWidth(80)
        self.para_filter.addItem("All", None)
        for p in PARA_OPTIONS:
            self.para_filter.addItem(p)
            
        self.dept_filter.currentIndexChanged.connect(self._do_search)
        self.para_filter.currentIndexChanged.connect(self._do_search)

        row1.addWidget(dept_lbl)
        self.dept_filter.setMaximumWidth(400)
        row1.addWidget(self.dept_filter)
        row1.addStretch()

        search_vbox.addLayout(row1)

        top_layout.addWidget(search_widget, stretch=1)

        # Envelope preview panel has been removed per user request

        root.addLayout(top_layout)

        # ── Bottom Section (Table) ──────────────────────────────────
        bottom_widget = QWidget()
        bottom_widget.setStyleSheet(f"background-color: {COLORS['surface']};")
        bottom_vbox = QVBoxLayout(bottom_widget)
        bottom_vbox.setContentsMargins(12, 6, 12, 8)
        bottom_vbox.setSpacing(6)

        # Selection Controls (Hidden by default)
        self.selection_controls_widget = QWidget()
        self.selection_controls_widget.setStyleSheet(f"background-color: {COLORS['surface']}; border: 1px solid #ddd; border-radius: 6px;")
        selection_layout = QVBoxLayout(self.selection_controls_widget)
        selection_layout.setContentsMargins(8, 8, 8, 8)
        selection_layout.setSpacing(6)
        
        # Row 1: Action Buttons
        action_row = QHBoxLayout()
        btn_style = "QPushButton { color: #333333; background-color: #FAFAFA; border: 1px solid #CCC; border-radius: 4px; padding: 6px 12px; font-weight: bold; } QPushButton:hover { background-color: #EEE; }"
        primary_btn_style = "QPushButton { background-color: #7A1212; color: white; border: 1px solid #7A1212; border-radius: 4px; padding: 6px 12px; font-weight: bold; } QPushButton:hover { background-color: #5C0D0D; }"
        
        self.btn_select_all = QPushButton("☑ Select All Rows")
        self.btn_select_all.setStyleSheet(btn_style)
        self.btn_select_all.clicked.connect(self._select_all_records)
        
        self.btn_deselect_all = QPushButton("☐ Deselect All Rows")
        self.btn_deselect_all.setStyleSheet(btn_style)
        self.btn_deselect_all.clicked.connect(self._deselect_all_records)
        
        self.btn_cancel_selection = QPushButton("🔄 Cancel Selection")
        self.btn_cancel_selection.setStyleSheet(btn_style)
        self.btn_cancel_selection.clicked.connect(self._cancel_selection_mode)
        
        self.btn_print_selected = QPushButton("🖨 Print Selected")
        self.btn_print_selected.setStyleSheet(primary_btn_style)
        self.btn_print_selected.clicked.connect(self._print_selected_list)
        
        lbl_info = QLabel("<b>1.</b> Select rows from table below.")
        lbl_info.setStyleSheet("color: #444;")
        
        action_row.addWidget(lbl_info)
        action_row.addStretch(1)
        action_row.addWidget(self.btn_select_all)
        action_row.addWidget(self.btn_deselect_all)
        action_row.addWidget(self.btn_cancel_selection)
        action_row.addWidget(self.btn_print_selected)
        selection_layout.addLayout(action_row)
        
        selection_layout.addWidget(HLine())
        
        # Row 2: Field Checkboxes
        self.fields_container = QWidget()
        fields_row = QHBoxLayout(self.fields_container)
        fields_row.setContentsMargins(0, 0, 0, 0)
        lbl_fields = QLabel("<b>2.</b> Select fields to print:")
        lbl_fields.setStyleSheet("color: #444;")
        fields_row.addWidget(lbl_fields)
        
        self.field_checkboxes = {}
        self.field_definitions = [
            ("dept_name", "Dept"),
            ("designation", "Designation"),
            ("office_name", "Office"),
            ("address", "Address"),
            ("city_state", "City/State"),
            ("pin_code", "PIN"),
            ("email", "Email"),
            ("contact_no", "Contact"),
            ("fax", "Fax"),
        ]
        
        for key, label in self.field_definitions:
            cb = QCheckBox(label)
            cb.setChecked(True)
            cb.setStyleSheet("padding-right: 8px;")
            self.field_checkboxes[key] = cb
            fields_row.addWidget(cb)
            
        fields_row.addStretch(1)
        selection_layout.addWidget(self.fields_container)
        
        self.selection_controls_widget.setVisible(False)
        bottom_vbox.addWidget(self.selection_controls_widget)

        # Address table
        self.table = QTableWidget()
        self.table.setColumnCount(len(TABLE_COLUMNS))
        self.table.setHorizontalHeaderLabels([c[0] for c in TABLE_COLUMNS])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(60)
        self.table.setSortingEnabled(True)
        self.table.itemSelectionChanged.connect(self._on_row_selected)
        self.table.itemChanged.connect(self._set_action_btns)

        # Hide ID column
        self.table.setColumnHidden(0, True)
        
        # Hide Edit column if user is not an admin
        if self.role != "admin":
            for col_idx, (_, key) in enumerate(TABLE_COLUMNS):
                if key == "edit_action":
                    self.table.setColumnHidden(col_idx, True)

        bottom_vbox.addWidget(self.table, stretch=1)

        # Print List and Label Buttons at bottom right
        bottom_action_row = QHBoxLayout()
        bottom_action_row.addStretch(1)
        
        btn_action_style = (
            "QPushButton {"
            "  background-color: #7A1212;"
            "  color: #FFFFFF;"
            "  border: 1px solid #7A1212;"
            "  border-radius: 6px;"
            "  font-size: 13px;"
            "  font-weight: bold;"
            "  padding: 8px 16px;"
            "}"
            "QPushButton:hover {"
            "  background-color: #5C0D0D;"
            "}"
        )

        self.btn_print_label_corner = QPushButton("🏷️ Print Reference Label(s) / संदर्भ लेबल (केवल NO:- Date)")
        self.btn_print_label_corner.setCursor(Qt.PointingHandCursor)
        self.btn_print_label_corner.setStyleSheet(btn_action_style)
        self.btn_print_label_corner.clicked.connect(lambda: self._enter_selection_mode("label"))
        
        self.btn_print_list_corner = QPushButton("📄 Print List / पता सूची प्रिंट करें")
        self.btn_print_list_corner.setCursor(Qt.PointingHandCursor)
        self.btn_print_list_corner.setStyleSheet(btn_action_style)
        self.btn_print_list_corner.clicked.connect(lambda: self._enter_selection_mode("list"))
        
        bottom_action_row.addWidget(self.btn_print_label_corner)
        bottom_action_row.addWidget(self.btn_print_list_corner)
        
        bottom_vbox.addLayout(bottom_action_row)
        root.addWidget(bottom_widget, stretch=1)


    def _handle_row_action(self, action, row_idx):
        rec_id = int(self.table.item(row_idx, 0).text())
        record = next((r for r in self._all_records if r["id"] == rec_id), None)
        if not record:
            return
            
        if action == "view":
            self._selected_record = record
            self._view_selected()
        elif action == "edit":
            self.edit_record.emit(record)
        elif action == "delete":
            self._selected_record = record
            self._delete_selected()

    def _clear_selection(self):
        self.table.clearSelection()

    def _load_dept_filter(self):
        self.dept_filter.clear()
        self.dept_filter.addItem("All Departments / सभी विभाग", None)
        depts = get_all_departments()
        self._dept_id_map = {}
        for d in depts:
            label = f"{d['dept_name']} ({d['dept_name_hindi']})"
            self.dept_filter.addItem(label, d["dept_id"])
            self._dept_id_map[d["dept_id"]] = d["dept_name"]

    def _load_records(self, records: list = None):
        if records is None:
            records = get_all_addresses()
        self._records = records
        self._populate_table(records)
        stats = get_address_stats()
        self.stats_lbl.setText(
            f"Total: {stats['total']} / 500 records | "
            f"Showing: {len(records)}"
        )
        is_full = stats['total'] >= 500
        if hasattr(self, 'add_btn'):
            self.add_btn.setEnabled(not is_full)
            if is_full:
                self.add_btn.setToolTip("Database Full (500/500) / डेटाबेस पूर्ण (500/500)")
            else:
                self.add_btn.setToolTip("Add new address record / नया पता रिकॉर्ड जोड़ें")

    def _populate_table(self, records: list):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        for row_idx, rec in enumerate(records):
            self.table.insertRow(row_idx)
            self.table.setRowHeight(row_idx, 55)
            for col_idx, (_, key) in enumerate(TABLE_COLUMNS):
                if key == "select":
                    item = QTableWidgetItem()
                    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    item.setCheckState(Qt.Unchecked)
                    item.setData(Qt.UserRole, rec)
                    self.table.setItem(row_idx, col_idx, item)
                    continue
                if key == "actions":
                    container = QWidget()
                    container_layout = QHBoxLayout(container)
                    container_layout.setContentsMargins(0, 0, 0, 0)
                    container_layout.setAlignment(Qt.AlignCenter)
                    
                    btn = QPushButton("View")
                    btn.setFixedSize(70, 28)
                    btn.setStyleSheet(
                        "QPushButton {"
                        "  background-color: #1a237e;"
                        "  color: white;"
                        "  border: none;"
                        "  border-radius: 14px;"
                        "  font-weight: bold;"
                        "  font-size: 12px;"
                        "  padding: 2px 12px;"
                        "}"
                        "QPushButton:hover {"
                        "  background-color: #121856;"
                        "}"
                    )
                    btn.clicked.connect(lambda checked=False, r=rec: self._view_single_record(r))
                    container_layout.addWidget(btn)
                    
                    self.table.setCellWidget(row_idx, col_idx, container)
                    
                    item = QTableWidgetItem()
                    item.setData(Qt.UserRole, rec)
                    self.table.setItem(row_idx, col_idx, item)
                    continue
                if key == "print_action":
                    container = QWidget()
                    container_layout = QHBoxLayout(container)
                    container_layout.setContentsMargins(0, 0, 0, 0)
                    container_layout.setAlignment(Qt.AlignCenter)
                    
                    btn = QPushButton("Print")
                    btn.setFixedSize(70, 28)
                    btn.setStyleSheet(
                        "QPushButton {"
                        "  background-color: #7A1212;"
                        "  color: white;"
                        "  border: none;"
                        "  border-radius: 14px;"
                        "  font-weight: bold;"
                        "  font-size: 12px;"
                        "  padding: 2px 12px;"
                        "}"
                        "QPushButton:hover {"
                        "  background-color: #5C0D0D;"
                        "}"
                    )
                    btn.clicked.connect(lambda checked=False, r=rec: self._print_single_record(r))
                    container_layout.addWidget(btn)
                    
                    self.table.setCellWidget(row_idx, col_idx, container)
                    
                    item = QTableWidgetItem()
                    item.setData(Qt.UserRole, rec)
                    self.table.setItem(row_idx, col_idx, item)
                    continue
                if key == "open_action":
                    container = QWidget()
                    container_layout = QHBoxLayout(container)
                    container_layout.setContentsMargins(0, 0, 0, 0)
                    container_layout.setAlignment(Qt.AlignCenter)
                    
                    btn = QPushButton("Open")
                    btn.setFixedSize(70, 28)
                    btn.setStyleSheet(
                        "QPushButton {"
                        "  background-color: white;"
                        "  color: #2196F3;"
                        "  border: 1px solid #BBDEFB;"
                        "  border-radius: 14px;"
                        "  font-weight: bold;"
                        "  font-size: 12px;"
                        "  padding: 2px 12px;"
                        "}"
                        "QPushButton:hover {"
                        "  background-color: #E3F2FD;"
                        "  border-color: #2196F3;"
                        "}"
                    )
                    btn.clicked.connect(lambda checked=False, r=rec: self._open_envelope_preview_for_record(r))
                    container_layout.addWidget(btn)
                    
                    self.table.setCellWidget(row_idx, col_idx, container)
                    
                    item = QTableWidgetItem()
                    item.setData(Qt.UserRole, rec)
                    self.table.setItem(row_idx, col_idx, item)
                    continue
                if key == "edit_action":
                    container = QWidget()
                    container_layout = QHBoxLayout(container)
                    container_layout.setContentsMargins(0, 0, 0, 0)
                    container_layout.setAlignment(Qt.AlignCenter)
                    
                    btn = QPushButton("Edit")
                    btn.setFixedSize(70, 28)
                    btn.setStyleSheet(
                        "QPushButton {"
                        "  background-color: #1f6b2e;"
                        "  color: white;"
                        "  border: none;"
                        "  border-radius: 14px;"
                        "  font-weight: bold;"
                        "  font-size: 12px;"
                        "  padding: 2px 12px;"
                        "}"
                        "QPushButton:hover {"
                        "  background-color: #154c20;"
                        "}"
                    )
                    btn.clicked.connect(lambda checked=False, r=rec: self.edit_record.emit(r))
                    container_layout.addWidget(btn)
                    
                    self.table.setCellWidget(row_idx, col_idx, container)
                    
                    item = QTableWidgetItem()
                    item.setData(Qt.UserRole, rec)
                    self.table.setItem(row_idx, col_idx, item)
                    continue
                val = str(rec.get(key, ""))
                if key == "date_entry":
                    try:
                        d = datetime.strptime(val, "%Y-%m-%d")
                        val = d.strftime("%d-%m-%Y")
                    except Exception:
                        pass
                if key == "delivery_type":
                    val = val[:15]  # Truncate for display
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                item.setData(Qt.UserRole, rec)
                self.table.setItem(row_idx, col_idx, item)
        self.table.resizeColumnsToContents()
        self.table.verticalHeader().setDefaultSectionSize(48)
        self.table.setSortingEnabled(True)

    def _do_search(self):
        dept_id = self.dept_filter.currentData()
        para    = self.para_filter.currentText()
        para    = para if para != "All" else ""
        
        results = search_addresses(
            dept_id=dept_id,
            para_no=para,
            keyword="",
            city="",
            pin_code="",
            date_entry=""
        )
        self._load_records(results)

    def _clear_search(self):
        self.dept_filter.blockSignals(True)
        self.para_filter.blockSignals(True)
        self.dept_filter.setCurrentIndex(0)
        self.para_filter.setCurrentIndex(0)
        self.dept_filter.blockSignals(False)
        self.para_filter.blockSignals(False)
        self._load_records()

    def _on_row_selected(self):
        rows = self.table.selectedItems()
        if not rows:
            self._selected_record = None
            self._update_preview()
            self._set_action_btns(False)
            return
        rec = self.table.item(rows[0].row(), 0).data(Qt.UserRole)
        self._selected_record = rec
        self._update_preview()
        self._set_action_btns(True)

    def _get_preview_html(self, rec: dict, is_dialog: bool = False, paper_size: str = "a4") -> str:
        ref_no = format_ref_no(rec.get("para_no", ""), rec.get("date_entry", ""), rec.get("ref_suffix", ""))
        sp  = rec.get("delivery_type", "Ordinary / साधारण")
        sp_eng = sp.split("/")[0].strip()
        sp_hin = sp.split("/")[1].strip() if len(sp.split("/")) > 1 else ""

        # Split ref_no
        ref_parts = ref_no.split("\n")
        no_line = ref_parts[0]
        date_line = ref_parts[1].replace("Date:- ", "Date:-") if len(ref_parts) > 1 else ""

        right_text = f"By S/P:- {sp_eng}/{sp_hin}" if sp_hin else f"By S/P:- {sp_eng}/"

        addr_lines = []
        to_val = rec.get("to_field", "").strip()
        if to_val and to_val.lower() not in ["to", "to,"]:
            addr_lines.append(to_val)
        if rec.get("designation"):
            addr_lines.append(rec['designation'])
        if rec.get("office_name"):
            addr_lines.append(rec['office_name'])
        if rec.get("addr_line1"):
            addr_lines.append(rec['addr_line1'])
        if rec.get("addr_line2"):
            addr_lines.append(rec['addr_line2'])
        
        city_state = ", ".join(filter(None, [rec.get("city",""), rec.get("state","")]))
        if city_state:
            addr_lines.append(city_state)
        if rec.get("pin_code"):
            addr_lines.append(f"PIN Code: {rec['pin_code']}")

        no_line_wrapped = wrap_text_html_fonts(no_line)
        date_line_wrapped = wrap_text_html_fonts(date_line)
        right_text_wrapped = wrap_text_html_fonts(right_text)
        to_label_wrapped = wrap_text_html_fonts("To,")
        
        addr_lines_wrapped = [wrap_text_html_fonts(line) for line in addr_lines]
        
        import os
        import sys
        if hasattr(sys, '_MEIPASS'):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(base_dir, "assets", "adrde_logo.png").replace('\\', '/')

        is_env = (paper_size == "envelope")
        logo_width = "300" if is_env else "400"
        
        sender_html = f'''
        <div style="display: inline-block; margin-left: 80px;">
            <img src="file:///{logo_path}" width="{logo_width}" />
        </div>
        '''
        
        address_html = f"<div>{to_label_wrapped}</div>\n"
        address_html += "<div style='margin-left: 25px;'>\n"
        for line in addr_lines_wrapped:
            address_html += f"<div>{line}</div>\n"
        address_html += "</div>\n"
            
        if is_env:
            font_size = "11pt"
            margin_bottom = "15px"
            body_padding = "20px"
        else:
            font_size = "14pt" if is_dialog else "13pt"
            margin_bottom = "40px" if is_dialog else "10px"
            body_padding = "40px" if is_dialog else "0px"
        
        html = f"""
        <html>
        <body style="margin: 0; padding: {body_padding}; background-color: transparent;">
            <div style="font-family: Arial, Mangal, sans-serif; font-size: {font_size}; line-height: 1.5;">
                <table width="100%" style="font-family: Arial, Mangal, sans-serif; font-size: {font_size}; color: #1a237e; font-weight: bold; border-collapse: collapse; margin-bottom: {margin_bottom};">
                    <tr>
                        <td align="left" valign="top" width="50%" style="border: none; padding: 0;">
                            <div style="margin-bottom: 15px;">{no_line_wrapped}</div>
                            <div>{date_line_wrapped}</div>
                        </td>
                        <td align="right" valign="top" width="50%" style="border: none; padding: 0;">{right_text_wrapped}</td>
                    </tr>
                </table>
                <table width="100%" style="font-family: Arial, Mangal, sans-serif; font-size: {font_size}; border-collapse: collapse; margin-bottom: 10px;">
                    <tr>
                        <td width="50%" style="border: none; padding: 0;"></td>
                        <td valign="top" style="color: #000000; border: none; padding: 0;">
                            {address_html}
                        </td>
                    </tr>
                </table>
                <table width="100%" style="font-family: Arial, Mangal, sans-serif; font-size: {font_size}; color: #1a237e; font-weight: bold; border-collapse: collapse;">
                    <tr>
                        <td align="left" valign="bottom" width="100%" style="border: none; padding: 0;">{sender_html}</td>
                    </tr>
                </table>
            </div>
        </body>
        </html>
        """
        return html

    def _update_preview(self):
        if hasattr(self, 'envelope_preview'):
            if not self._selected_record:
                self.envelope_preview.setPlainText(
                    "← Select a record to preview the envelope.\n← पता देखने के लिए रिकॉर्ड चुनें।"
                )
                return
            rec = self._selected_record.copy()
            html = self._get_preview_html(rec, is_dialog=False)
            self.envelope_preview.setHtml(html)

    def _on_row_double_clicked(self):
        self._view_selected()

    def _set_action_btns(self, *args, **kwargs):
        checked = self._get_checked_records()
        sel_count = len(checked)
        
        if sel_count == 0 and self._selected_record:
            sel_count = 1

        if sel_count == 0:
            if hasattr(self, 'view_btn'): self.view_btn.setEnabled(False)
            if hasattr(self, 'preview_open_btn'): self.preview_open_btn.setEnabled(False)
            if self.role == "admin":
                if hasattr(self, 'edit_btn'): self.edit_btn.setEnabled(False)
                if hasattr(self, 'del_btn'): self.del_btn.setEnabled(False)
            return

        if hasattr(self, 'view_btn'): self.view_btn.setEnabled(True)
        if hasattr(self, 'preview_open_btn'): self.preview_open_btn.setEnabled(sel_count == 1)
        if self.role == "admin":
            if hasattr(self, 'edit_btn'): self.edit_btn.setEnabled(sel_count == 1)
            if hasattr(self, 'del_btn'): self.del_btn.setEnabled(sel_count >= 1)

    def _get_checked_records(self) -> list[dict]:
        checked = []
        for r in range(self.table.rowCount()):
            # We search for item in the checkable column
            # Note: Select column is at index 1 in TABLE_COLUMNS
            item = self.table.item(r, 1)
            if item and item.checkState() == Qt.Checked:
                rec = item.data(Qt.UserRole)
                if rec:
                    checked.append(rec)
        return checked

    def _view_selected(self):
        checked = self._get_checked_records()
        records_to_view = checked if checked else ([self._selected_record] if self._selected_record else [])
        if not records_to_view:
            return

        if len(records_to_view) > 10:
            show_warning(self, "Limit Exceeded / सीमा पार", "You can view at most 10 records at once.\nआप एक बार में अधिकतम 10 रिकॉर्ड देख सकते हैं।")
            records_to_view = records_to_view[:10]

        from ui.address_form import AddressForm
        if not hasattr(self, "_active_view_forms"):
            self._active_view_forms = []

        for rec in records_to_view:
            form = AddressForm(mode="view", record=rec)
            form.cancelled.connect(form.close)
            form.setWindowFlags(Qt.Window)
            form.resize(850, 700)
            form.setWindowTitle(f"View Address: {rec.get('office_name','')} / पता देखें")
            form.show()
            self._active_view_forms.append(form)
            # Remove from references when closed
            form.destroyed.connect(lambda f=form: self._active_view_forms.remove(f) if f in self._active_view_forms else None)

    def _edit_selected(self):
        if not self._selected_record:
            return
        self.edit_record.emit(self._selected_record)

    def _delete_selected(self):
        checked = self._get_checked_records()
        if checked:
            if show_question(
                self,
                "Confirm Delete / हटाने की पुष्टि",
                f"Are you sure you want to delete these {len(checked)} records?\n"
                f"क्या आप इन {len(checked)} रिकॉर्ड को हटाना चाहते हैं?"
            ):
                success_count = 0
                for rec in checked:
                    ok, _ = delete_address(rec["id"])
                    if ok:
                        success_count += 1
                show_info(self, "Deleted / हटाया गया", f"Successfully deleted {success_count} of {len(checked)} records.\n{success_count} रिकॉर्ड सफलतापूर्वक हटाए गए।")
                self._load_records()
                self._selected_record = None
                self._update_preview()
            return

        if not self._selected_record:
            return
        rec = self._selected_record
        if show_question(
            self,
            "Confirm Delete / हटाने की पुष्टि",
            f"Are you sure you want to delete this record?\n"
            f"क्या आप इस रिकॉर्ड को हटाना चाहते हैं?\n\n"
            f"Office: {rec.get('office_name','')}\n"
            f"City: {rec.get('city','')}"
        ):
            ok, msg = delete_address(rec["id"])
            if ok:
                show_info(self, "Deleted / हटाया गया", msg)
                self._load_records()
                self._selected_record = None
                self._update_preview()
            else:
                show_error(self, "Error / त्रुटि", msg)

    def _get_print_path(self, suffix: str, default_ext=".pdf", no_dialog=False) -> str | None:
        out_dir = get_default_output_dir()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = os.path.join(out_dir, f"ADRDE_{suffix}_{ts}{default_ext}")
        if no_dialog:
            return default_name
            
        ext_filter = "PDF Files (*.pdf)" if default_ext == ".pdf" else "Excel Files (*.xlsx)"
        title = "Save PDF / PDF सहेजें" if default_ext == ".pdf" else "Save Excel / Excel सहेजें"
        path, _ = QFileDialog.getSaveFileName(
            self, title,
            default_name,
            ext_filter
        )
        return path if path else None

    def _get_record_for_print(self, record: dict) -> dict:
        """Get record with preview panel overrides applied."""
        return record.copy()

    def _print_single(self):
        if not self._selected_record:
            return
        rec = self._get_record_for_print(self._selected_record)
        
        dlg = EnvelopeReferenceDialog(self, [rec])
        if dlg.exec() != QDialog.Accepted:
            return
            
        vals = dlg.get_values_list()[0]
        rec_copy = rec.copy()
        rec_copy.update(vals)
        
        from modules.address_ops import update_address
        update_address(rec_copy["id"], rec_copy)
        self._load_records()
        self._selected_record = rec_copy
        self._update_preview()
        
        if dlg.get_selected_action() == "save":
            return
            
        from modules.export_action import execute_export_action
        from modules.print_module import generate_single_envelope_pdf
        execute_export_action(
            parent_widget=self,
            records=[rec_copy],
            pdf_suffix="Envelope",
            pdf_generator_func=lambda path: generate_single_envelope_pdf(rec_copy, path),
            is_envelope_or_label=True
        )

    def _view_single_record(self, rec: dict):
        from ui.address_form import AddressForm
        if not hasattr(self, "_active_view_forms"):
            self._active_view_forms = []
            
        form = AddressForm(mode="view", record=rec)
        form.cancelled.connect(form.close)
        form.setWindowFlags(Qt.Window)
        form.resize(850, 700)
        form.setWindowTitle(f"View Address: {rec.get('office_name','')} / पता देखें")
        form.show()
        self._active_view_forms.append(form)
        form.destroyed.connect(lambda f=form: self._active_view_forms.remove(f) if f in self._active_view_forms else None)

    def _print_single_record(self, rec: dict):
        dlg = EnvelopeReferenceDialog(self, [rec])
        if dlg.exec() != QDialog.Accepted:
            return
            
        vals = dlg.get_values_list()[0]
        rec_copy = rec.copy()
        rec_copy.update(vals)
        
        from modules.address_ops import update_address
        update_address(rec_copy["id"], rec_copy)
        self._load_records()
        self._selected_record = rec_copy
        self._update_preview()
        
        if dlg.get_selected_action() == "save":
            return
            
        from modules.export_action import execute_export_action
        from modules.print_module import generate_single_envelope_pdf
        execute_export_action(
            parent_widget=self,
            records=[rec_copy],
            pdf_suffix="Envelope",
            pdf_generator_func=lambda path: generate_single_envelope_pdf(rec_copy, path),
            is_envelope_or_label=True
        )

    def _print_checked(self):
        checked = self._get_checked_records()
        if not checked:
            return
            
        dlg = EnvelopeReferenceDialog(self, checked)
        if dlg.exec() != QDialog.Accepted:
            return
            
        vals_list = dlg.get_values_list()
        recs = []
        from modules.address_ops import update_address
        for i, r in enumerate(checked):
            r_copy = self._get_record_for_print(r)
            r_copy.update(vals_list[i])
            update_address(r_copy["id"], r_copy)
            recs.append(r_copy)
            
        self._load_records()
        self._selected_record = None
        self._update_preview()
        
        if dlg.get_selected_action() == "save":
            return
            
        from modules.export_action import execute_export_action
        from modules.print_module import generate_multiple_envelopes_pdf
        execute_export_action(
            parent_widget=self,
            records=recs,
            pdf_suffix="Multiple_Envelopes",
            pdf_generator_func=lambda path: generate_multiple_envelopes_pdf(recs, path),
            is_envelope_or_label=True
        )

    def _print_label(self):
        checked = self._get_checked_records()
        if checked:
            recs = [self._get_record_for_print(r) for r in checked]
            from modules.export_action import execute_export_action
            from modules.print_module import generate_multiple_labels_pdf
            execute_export_action(
                parent_widget=self,
                records=recs,
                pdf_suffix="Multiple_Labels",
                pdf_generator_func=lambda path: generate_multiple_labels_pdf(recs, path),
                is_envelope_or_label=True
            )
            return

        if not self._selected_record:
            return
        rec = self._get_record_for_print(self._selected_record)
        from modules.export_action import execute_export_action
        from modules.print_module import generate_single_label_pdf
        execute_export_action(
            parent_widget=self,
            records=[rec],
            pdf_suffix="Label",
            pdf_generator_func=lambda path: generate_single_label_pdf(rec, path),
            is_envelope_or_label=True
        )

    def _show_print_dialog(self):
        has_selected = self._selected_record is not None
        has_checked = len(self._get_checked_records()) > 0
        
        # Check if a department is selected in the search filters
        dept_id = self.dept_filter.currentData()
        has_dept = dept_id is not None and dept_id != ""

        dlg = PrintOptionsDialog(self, has_selected, has_checked, has_dept)
        if dlg.exec() == QDialog.Accepted:
            opt = dlg.selected_option
            if opt == "envelope":
                checked = self._get_checked_records()
                if checked:
                    self._print_checked()
                else:
                    self._print_single()
            elif opt == "dept":
                self._print_dept()
            elif opt == "all":
                self._print_all()

    def _enter_selection_mode(self, mode="list"):
        self.current_selection_mode = mode
        self.btn_print_list_corner.setVisible(False)
        self.btn_print_label_corner.setVisible(False)
        self.selection_controls_widget.setVisible(True)
        if mode == "label":
            self.fields_container.setVisible(False)
            self.btn_print_selected.setText("🖨 Print Selected Labels")
        else:
            self.fields_container.setVisible(True)
            self.btn_print_selected.setText("🖨 Print Selected List")

    def _cancel_selection_mode(self):
        self.selection_controls_widget.setVisible(False)
        self.btn_print_list_corner.setVisible(True)
        self.btn_print_label_corner.setVisible(True)
        self._deselect_all_records()

    def _select_all_records(self):
        self.table.blockSignals(True)
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)
            if item:
                item.setCheckState(Qt.Checked)
        self.table.blockSignals(False)
        self._set_action_btns()

    def _deselect_all_records(self):
        self.table.blockSignals(True)
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)
            if item:
                item.setCheckState(Qt.Unchecked)
        self.table.blockSignals(False)
        self._set_action_btns()

    def _print_selected_list(self):
        checked = self._get_checked_records()
        if not checked:
            show_warning(self, "No Selection", "Please select at least one address to print.")
            return
            
        if getattr(self, "current_selection_mode", "list") == "label":
            # Show preview dialog first
            dialog = ReferenceLabelPreviewDialog(self, checked)
            if dialog.exec() == QDialog.Accepted:
                from modules.export_action import execute_export_action
                from modules.print_module import generate_reference_labels_pdf
                execute_export_action(
                    parent_widget=self,
                    records=checked,
                    pdf_suffix="ReferenceLabels",
                    pdf_generator_func=lambda path: generate_reference_labels_pdf(checked, path, dialog.selected_print_mode),
                    is_envelope_or_label=True
                )
                self._cancel_selection_mode()
            return

        selected_cols = [key for key, _ in self.field_definitions if self.field_checkboxes[key].isChecked()]
        if not selected_cols:
            show_warning(self, "No Columns Selected", "Please select at least one column to print.")
            return
            
        from modules.export_action import execute_export_action
        from modules.print_module import generate_address_list_pdf
        excel_cols = [(header, key) for header, key in self.field_definitions if key in selected_cols]
        execute_export_action(
            parent_widget=self,
            records=checked,
            pdf_suffix="AddressList",
            pdf_generator_func=lambda path: generate_address_list_pdf(checked, path, selected_cols),
            excel_columns=excel_cols
        )
        self._cancel_selection_mode()

    def _print_list(self):
        checked = self._get_checked_records()
        records = checked if checked else (
            [self._selected_record] if self._selected_record else self._records
        )
        if not records:
            show_info(self, "No Records", LABELS["no_records"])
            return
            
        dlg = ColumnSelectionDialog(self)
        if dlg.exec() != QDialog.Accepted:
            return
            
        selected_cols = dlg.get_selected_columns()
        if not selected_cols:
            show_warning(self, "No Columns Selected / कोई कॉलम नहीं चुना गया", "Please select at least one column to print.")
            return
            
        from modules.export_action import execute_export_action
        from modules.print_module import generate_address_list_pdf
        excel_cols = [(header, key) for header, key in self.field_definitions if key in selected_cols]
        execute_export_action(
            parent_widget=self,
            records=records,
            pdf_suffix="AddressList",
            pdf_generator_func=lambda path: generate_address_list_pdf(records, path, selected_cols),
            excel_columns=excel_cols
        )

    def _print_dept(self):
        dept_id = self.dept_filter.currentData()
        dept_name = self.dept_filter.currentText()
        if not dept_id:
            show_warning(self, "Select Department / विभाग चुनें",
                         "Please select a specific department first.\nकृपया पहले एक विभाग चुनें।")
            return
        records = get_all_addresses(dept_id=dept_id)
        if not records:
            show_info(self, "No Records", LABELS["no_records"])
            return
            
        from modules.export_action import execute_export_action
        from modules.print_module import generate_department_list_pdf
        excel_cols = [(header, key) for header, key in self.field_definitions if key not in ("select", "actions", "id")]
        execute_export_action(
            parent_widget=self,
            records=records,
            pdf_suffix=f"Dept_{dept_name.split('(')[0].strip()}",
            pdf_generator_func=lambda path: generate_department_list_pdf(records, dept_name, path),
            excel_columns=excel_cols
        )

    def _print_all(self):
        records = get_all_addresses()
        if not records:
            show_info(self, "No Records", LABELS["no_records"])
            return
            
        from modules.export_action import execute_export_action
        from modules.print_module import generate_full_directory_pdf
        excel_cols = [(header, key) for header, key in self.field_definitions if key not in ("select", "actions", "id")]
        execute_export_action(
            parent_widget=self,
            records=records,
            pdf_suffix="FullDirectory",
            pdf_generator_func=lambda path: generate_full_directory_pdf(records, path),
            excel_columns=excel_cols
        )

    def refresh(self):
        """Reload all records from DB."""
        self._load_records()

    def _open_envelope_preview_for_record(self, record):
        self._selected_record = record
        self._open_envelope_preview_dialog()

    def _open_envelope_preview_dialog(self):
        if not self._selected_record:
            return
        html = self._get_preview_html(self._selected_record, is_dialog=True)

        dialog = QDialog(self)
        dialog.setWindowTitle("Envelope Preview / लिफाफा पूर्वावलोकन")
        dialog.resize(850, 480)
        
        layout = QVBoxLayout(dialog)
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
        
        preview_text = ZoomablePreview(html)
        preview_text.setStyleSheet("""
            QGraphicsView {
                border: 1px solid #CCCCCC;
                border-radius: 8px;
            }
        """)
        
        layout.addWidget(preview_text, stretch=1)
        
        btn_box = QDialogButtonBox(QDialogButtonBox.Close)
        
        print_btn = QPushButton("🖨️ Print Envelope / लिफाफा प्रिंट करें")
        print_btn.setStyleSheet("background-color: #7A1212; color: white; padding: 6px 16px; font-weight: bold; border-radius: 4px;")
        
        def print_from_preview():
            dialog.accept()
            self._print_single()
            
        print_btn.clicked.connect(print_from_preview)
        btn_box.addButton(print_btn, QDialogButtonBox.ActionRole)
        
        btn_box.rejected.connect(dialog.accept)
        layout.addWidget(btn_box)
        
        dialog.exec()
