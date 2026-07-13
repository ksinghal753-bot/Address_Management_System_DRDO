"""
Address Form — Add / Edit address with all 10 fields.
Admin only for add/edit. Reads-only for view mode.
"""

from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QLineEdit, QComboBox, QListView, QCalendarWidget, QStyleFactory, QDateEdit, QPushButton, QGroupBox,
    QScrollArea, QFrame, QSizePolicy, QDialog, QDialogButtonBox,
    QMessageBox, QTextEdit, QGridLayout
)
from PySide6.QtCore import Qt, Signal, QDate
from PySide6.QtGui import QFont

from modules.address_ops import add_address, update_address, get_address_stats
from modules.department_ops import get_all_departments
from modules.print_module import format_ref_no, get_default_output_dir
from ui.shared_widgets import HeaderBar, SectionTitle, HLine, show_error, show_info, show_warning
from utils.constants import COLORS, LABELS, PARA_OPTIONS, DELIVERY_TYPES, ENVELOPE_PREFIX
from utils.validators import (
    validate_required, validate_pin_code, validate_email,
    validate_fax, validate_contact
)


def _field_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setObjectName("fieldLabel")
    return lbl


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


class AddressForm(QWidget):
    """
    10-field address entry/edit form.
    mode: 'add' | 'edit' | 'view'
    Emits saved() when record is successfully saved.
    Emits cancelled() on cancel.
    """
    saved     = Signal()
    cancelled = Signal()

    def __init__(self, mode: str = "add", record: dict = None, parent=None):
        super().__init__(parent)
        self.mode   = mode
        self.record = record or {}
        self._dept_map: dict[str, int] = {}
        self._build_ui()
        if record:
            self._populate(record)

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)



        # Scroll area for form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        container.setObjectName("formContainer")
        container.setStyleSheet(f"#formContainer {{ background-color: {COLORS['surface']}; }}")
        cl = QVBoxLayout(container)
        cl.setContentsMargins(30, 20, 30, 20)
        cl.setSpacing(16)

        # ── Title ─────────────────────────────────────────────────────────────
        mode_titles = {
            "add":  "Add New Address / नया पता जोड़ें",
            "edit": "Edit Address / पता संपादित करें",
            "view": "View Address / पता देखें",
        }
        title = SectionTitle(mode_titles.get(self.mode, "Address"))
        cl.addWidget(title)
        cl.addWidget(HLine())

        # ── Envelope reference row ────────────────────────────────────────────
        env_group = QGroupBox("Envelope Reference / लिफाफा संदर्भ")
        eg_layout = QHBoxLayout(env_group)
        eg_layout.setSpacing(16)

        # Left side vertical layout: NO.:- preview and Date picker
        left_layout = QVBoxLayout()
        left_layout.setSpacing(8)

        # Reference preview
        self.ref_preview = QLineEdit()
        self.ref_preview.setReadOnly(True)
        self.ref_preview.setStyleSheet(
            f"QLineEdit {{"
            f"  background-color: #FAFAFA;"
            f"  color: {COLORS['primary']};"
            f"  font-weight: bold;"
            f"  font-size: 13px;"
            f"  border: 1.5px solid {COLORS['border']};"
            f"  border-radius: 8px;"
            f"  padding: 5px 10px;"
            f"  min-height: 38px;"
            f"  min-width: 280px;"
            f"}}"
        )
        left_layout.addWidget(self.ref_preview)

        # Date picker below NO.:-
        date_row = QHBoxLayout()
        date_row.setSpacing(8)
        date_lbl = _field_label("Date / दिनांक *")
        self.date_edit = QDateEdit()
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
        border: none;
        outline: 0;
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
        self.date_edit.setCalendarWidget(cal)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd-MM-yyyy")
        self.date_edit.dateChanged.connect(self._update_ref_preview)
        date_row.addWidget(date_lbl)
        date_row.addWidget(self.date_edit)
        left_layout.addLayout(date_row)

        eg_layout.addLayout(left_layout)
        eg_layout.addSpacing(16)

        # PARA dropdown
        para_vbox = QVBoxLayout()
        para_vbox.setSpacing(4)
        para_lbl = _field_label("PARA No. / पैरा नं. *")
        self.para_combo = QComboBox()
        self.para_combo.setStyle(QStyleFactory.create('Fusion'))
        self.para_combo.setView(QListView())
        self.para_combo.addItems(PARA_OPTIONS)
        self.para_combo.setCurrentIndex(0)
        self.para_combo.currentIndexChanged.connect(self._update_ref_preview)
        para_vbox.addWidget(para_lbl)
        para_vbox.addWidget(self.para_combo)
        eg_layout.addLayout(para_vbox)

        # Writable Textarea in place of Date
        suffix_vbox = QVBoxLayout()
        suffix_vbox.setSpacing(4)
        suffix_lbl = _field_label("Custom Text / अतिरिक्त पाठ")
        self.suffix_edit = QTextEdit()
        self.suffix_edit.setPlaceholderText("Write suffix here...")
        self.suffix_edit.setFixedHeight(38)
        self.suffix_edit.setStyleSheet(
            f"QTextEdit {{"
            f"  background: #FFFFFF;"
            f"  border: 1.5px solid {COLORS['border']};"
            f"  border-radius: 8px;"
            f"  padding: 5px 10px;"
            f"  font-size: 13px;"
            f"  color: {COLORS['text_primary']};"
            f"}}"
        )
        self.suffix_edit.textChanged.connect(self._update_ref_preview)
        suffix_vbox.addWidget(suffix_lbl)
        suffix_vbox.addWidget(self.suffix_edit)
        eg_layout.addLayout(suffix_vbox)

        # Delivery type
        sp_vbox = QVBoxLayout()
        sp_vbox.setSpacing(4)
        sp_lbl = _field_label("By S/P / डाक प्रकार")
        self.sp_combo = QComboBox()
        self.sp_combo.setStyle(QStyleFactory.create('Fusion'))
        self.sp_combo.setView(QListView())
        self.sp_combo.addItems(DELIVERY_TYPES)
        sp_vbox.addWidget(sp_lbl)
        sp_vbox.addWidget(self.sp_combo)
        eg_layout.addLayout(sp_vbox)

        env_group.setVisible(False)
        cl.addWidget(env_group)

        # ── Department ────────────────────────────────────────────────────────
        dept_group = QGroupBox("Department / विभाग")
        dg = QHBoxLayout(dept_group)
        dept_lbl = _field_label("Department / विभाग *")
        self.dept_combo = QComboBox()
        self.dept_combo.setStyle(QStyleFactory.create('Fusion'))
        self.dept_combo.setView(QListView())
        self._load_departments()
        dg.addWidget(dept_lbl)
        dg.addWidget(self.dept_combo)
        dg.addStretch()
        cl.addWidget(dept_group)

        # ── Address fields ────────────────────────────────────────────────────
        addr_group = QGroupBox("Address Details / पता विवरण")
        grid = QGridLayout(addr_group)
        grid.setSpacing(12)
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(12)
        grid.setContentsMargins(20, 20, 20, 20)
        
        # Row 0: Designation & Designation Hindi (Left)
        self.to_field = QLineEdit()  # Kept hidden for backend compatibility
        
        grid.addWidget(_field_label("Designation / पदनाम *"), 0, 0, Qt.AlignRight | Qt.AlignVCenter)
        self.designation = QLineEdit()
        self.designation.setPlaceholderText("e.g. Director")
        self.designation_hi = QLineEdit()  # Kept hidden for compatibility
        grid.addWidget(self.designation, 0, 1)
        
        # Row 1: Office/Dept Name (Left) / Address Line 1 (Right)
        grid.addWidget(_field_label("Office/Dept Name / कार्यालय नाम *"), 1, 0, Qt.AlignRight | Qt.AlignVCenter)
        self.office_name = QLineEdit()
        self.office_name.setPlaceholderText("e.g. ADRDE, AS-QMS")
        grid.addWidget(self.office_name, 1, 1)
        
        grid.addWidget(_field_label("Address Line 1 / पता पंक्ति 1 *"), 1, 2, Qt.AlignRight | Qt.AlignVCenter)
        self.addr_line1 = QLineEdit()
        self.addr_line1.setPlaceholderText("e.g. PB No. 51, Station Road")
        grid.addWidget(self.addr_line1, 1, 3)
        
        # Row 2: Address Line 2 (Left) / City (Right)
        grid.addWidget(_field_label("Address Line 2 / पता पंक्ति 2"), 2, 0, Qt.AlignRight | Qt.AlignVCenter)
        self.addr_line2 = QLineEdit()
        self.addr_line2.setPlaceholderText("e.g. Near Airport")
        grid.addWidget(self.addr_line2, 2, 1)
        
        grid.addWidget(_field_label("City / शहर *"), 2, 2, Qt.AlignRight | Qt.AlignVCenter)
        self.city = QLineEdit()
        self.city.setPlaceholderText("e.g. Agra Cantt")
        grid.addWidget(self.city, 2, 3)

        # State
        grid.addWidget(_field_label("State / राज्य *"), 3, 0, Qt.AlignRight | Qt.AlignVCenter)
        self.state = QLineEdit()
        self.state.setPlaceholderText("e.g. UP")
        grid.addWidget(self.state, 3, 1)

        # Field 7: PIN Code
        grid.addWidget(_field_label("PIN Code / पिन कोड *"), 3, 2, Qt.AlignRight | Qt.AlignVCenter)
        self.pin_code = QLineEdit()
        self.pin_code.setPlaceholderText("e.g. 282001")
        self.pin_code.setMaxLength(6)
        grid.addWidget(self.pin_code, 3, 3)

        cl.addWidget(addr_group)

        # ── Contact Details (stored but NOT printed) ───────────────────────────
        contact_group = QGroupBox(
            "Contact Details (Stored Only / केवल संग्रहीत — Not Printed / प्रिंट नहीं होता)"
        )
        contact_group.setStyleSheet(
            f"QGroupBox {{ border: 1.5px dashed {COLORS['warning']}; color: {COLORS['warning']}; }}"
        )
        cf = QFormLayout(contact_group)
        cf.setSpacing(12)
        cf.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Field 8: Email
        self.email = QLineEdit()
        self.email.setPlaceholderText("e.g. director@adrde.drdo.in")
        cf.addRow(_field_label("Email / ईमेल"), self.email)

        # Field 9: FAX
        self.fax = QLineEdit()
        self.fax.setPlaceholderText("e.g. 0562-2401234")
        cf.addRow(_field_label("FAX No. / फैक्स नं."), self.fax)

        # Field 10: Contact
        self.contact_no = QLineEdit()
        self.contact_no.setPlaceholderText("e.g. +91-9876543210")
        cf.addRow(_field_label("Contact No. / संपर्क नं."), self.contact_no)

        warn_lbl = QLabel(
            "⚠️ These fields will NOT appear in any printout.\n"
            "⚠️ ये फ़ील्ड किसी भी प्रिंट में दिखाई नहीं देंगे।"
        )
        warn_lbl.setStyleSheet(
            f"color: {COLORS['warning']}; font-size: 11px; font-style: italic;"
        )
        cf.addRow("", warn_lbl)
        cl.addWidget(contact_group)

        # ── Envelope Preview ──────────────────────────────────────────────────
        prev_group = QGroupBox("Envelope Preview / लिफाफा पूर्वावलोकन")
        pvl = QVBoxLayout(prev_group)
        self.envelope_preview = QTextEdit()
        self.envelope_preview.setReadOnly(True)
        self.envelope_preview.setObjectName("envelopePreview")
        self.envelope_preview.setMinimumHeight(160)
        self.envelope_preview.setMaximumHeight(200)
        pvl.addWidget(self.envelope_preview)
        cl.addWidget(prev_group)

        # Connect all fields to preview update
        for field in [self.to_field, self.designation, self.designation_hi, self.office_name,
                      self.addr_line1, self.addr_line2, self.city, self.state, self.pin_code]:
            field.textChanged.connect(self._update_envelope_preview)

        # ── Buttons ───────────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        # Open envelope preview button
        self.open_preview_btn = QPushButton("👁️  Open / खोलें")
        self.open_preview_btn.setObjectName("secondaryButton")
        self.open_preview_btn.setMinimumHeight(42)
        self.open_preview_btn.clicked.connect(self._open_envelope_preview_dialog)

        if self.mode in ("add", "edit"):
            self.save_btn = QPushButton("💾  " + LABELS["save"])
            self.save_btn.setObjectName("successButton")
            self.save_btn.setMinimumHeight(42)
            self.save_btn.clicked.connect(self._save)

            self.clear_btn = QPushButton("🗑️  " + LABELS["clear"])
            self.clear_btn.setMinimumHeight(42)
            self.clear_btn.clicked.connect(self._clear)

            self.cancel_btn = QPushButton("✖  " + LABELS["cancel"])
            self.cancel_btn.setObjectName("dangerButton")
            self.cancel_btn.setMinimumHeight(42)
            self.cancel_btn.clicked.connect(self.cancelled.emit)

            btn_row.addWidget(self.open_preview_btn)
            btn_row.addWidget(self.save_btn)
            btn_row.addWidget(self.clear_btn)
            btn_row.addStretch()
            btn_row.addWidget(self.cancel_btn)
        else:
            # View mode
            close_btn = QPushButton("← " + LABELS["return"])
            close_btn.setMinimumHeight(42)
            close_btn.clicked.connect(self.cancelled.emit)
            btn_row.addWidget(self.open_preview_btn)
            btn_row.addStretch()
            btn_row.addWidget(close_btn)

        cl.addLayout(btn_row)
        cl.addSpacing(20)

        scroll.setWidget(container)
        root.addWidget(scroll, stretch=1)

        # Set read-only if view mode
        if self.mode == "view":
            self._set_readonly(True)

        if self.mode == "add":
            stats = get_address_stats()
            if stats["total"] >= 500:
                self.save_btn.setEnabled(False)
                self.save_btn.setToolTip("Database Full (500/500) / डेटाबेस पूर्ण (500/500)")

        self._update_ref_preview()
        self._update_envelope_preview()

    def _load_departments(self):
        self.dept_combo.clear()
        self._dept_map.clear()
        depts = get_all_departments()
        for d in depts:
            label = f"{d['dept_name']} ({d['dept_name_hindi']})"
            self.dept_combo.addItem(label)
            self._dept_map[label] = d["dept_id"]
        if self.record and self.record.get("dept_id"):
            for i, (label, did) in enumerate(self._dept_map.items()):
                if did == self.record["dept_id"]:
                    self.dept_combo.setCurrentIndex(i)
                    break

    def _update_ref_preview(self):
        para = self.para_combo.currentText()
        para_part = para.replace(" ", "").upper()
        suffix = self.suffix_edit.toPlainText().strip()
        if suffix:
            ref = f"NO.:- {ENVELOPE_PREFIX}/{para_part}/{suffix}"
        else:
            ref = f"NO.:- {ENVELOPE_PREFIX}/{para_part}"
        self.ref_preview.setText(ref)
        self._update_envelope_preview()

    def _get_preview_html(self, is_dialog: bool = False) -> str:
        para = self.para_combo.currentText()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        sp   = self.sp_combo.currentText()
        try:
            d = datetime.strptime(date, "%Y-%m-%d")
            date_str = d.strftime("%d-%m-%Y")
        except Exception:
            date_str = date
        para_part = para.replace(" ", "").upper()
        
        suffix = self.suffix_edit.toPlainText().strip()
        if suffix:
            ref = f"NO.:- {ENVELOPE_PREFIX}/{para_part}/{suffix}"
        else:
            ref = f"NO.:- {ENVELOPE_PREFIX}/{para_part}"
        date_line = f"Date:- {date_str}"

        sp_eng = sp.split("/")[0].strip()
        sp_hin = sp.split("/")[1].strip() if len(sp.split("/")) > 1 else ""

        right_text = f"By S/P:- {sp_eng}/{sp_hin}" if sp_hin else f"By S/P:- {sp_eng}/"

        addr_lines = []
        to_val = self.to_field.text().strip()
        if to_val and to_val.lower() not in ["to", "to,"]:
            addr_lines.append(to_val)
        if self.designation.text().strip():
            addr_lines.append(self.designation.text().strip())
        if self.office_name.text().strip():
            addr_lines.append(self.office_name.text().strip())
        if self.addr_line1.text().strip():
            addr_lines.append(self.addr_line1.text().strip())
        if self.addr_line2.text().strip():
            addr_lines.append(self.addr_line2.text().strip())

        city = self.city.text().strip()
        state = self.state.text().strip()
        if city or state:
            addr_lines.append(f"{', '.join(filter(None, [city, state]))}")

        pin = self.pin_code.text().strip()
        if pin:
            addr_lines.append(f"PIN Code: {pin}")

        ref_wrapped = wrap_text_html_fonts(ref)
        date_line_wrapped = wrap_text_html_fonts(date_line)
        right_text_wrapped = wrap_text_html_fonts(right_text)
        to_label_wrapped = wrap_text_html_fonts("To,")
        
        addr_lines_wrapped = [wrap_text_html_fonts(line) for line in addr_lines]
        
        address_html = f"<div>{to_label_wrapped}</div>\n"
        for line in addr_lines_wrapped:
            address_html += f"<div>{line}</div>\n"
            
        font_size = "14pt" if is_dialog else "13pt"
        margin_bottom = "40px" if is_dialog else "10px"
        body_padding = "40px" if is_dialog else "0px"
        
        html = f"""
        <html>
        <body style="margin: 0; padding: {body_padding}; background-color: transparent;">
            <div style="font-family: Arial, Mangal, sans-serif; font-size: {font_size}; line-height: 1.5;">
                <table width="100%" style="font-family: Arial, Mangal, sans-serif; font-size: {font_size}; color: #1a237e; font-weight: bold; border-collapse: collapse; margin-bottom: {margin_bottom};">
                    <tr>
                        <td align="left" style="border: none; padding: 0;">{ref_wrapped}<br/>{date_line_wrapped}</td>
                        <td align="right" valign="top" style="border: none; padding: 0;">{right_text_wrapped}</td>
                    </tr>
                </table>
                <br/>
                <table width="100%" style="font-family: Arial, Mangal, sans-serif; font-size: {font_size}; border-collapse: collapse;">
                    <tr>
                        <td width="45%" style="border: none; padding: 0;"></td>
                        <td valign="top" style="color: #000000; border: none; padding: 0;">
                            {address_html}
                        </td>
                    </tr>
                </table>
            </div>
        </body>
        </html>
        """
        return html

    def _update_envelope_preview(self):
        """Update the live envelope preview text."""
        html = self._get_preview_html(is_dialog=False)
        self.envelope_preview.setHtml(html)

    def _populate(self, record: dict):
        """Fill form fields from a record dict."""
        # PARA
        para = record.get("para_no", PARA_OPTIONS[0])
        idx = self.para_combo.findText(para)
        if idx >= 0:
            self.para_combo.setCurrentIndex(idx)

        # Date
        date_str = record.get("date_entry", "")
        if date_str:
            try:
                d = datetime.strptime(date_str, "%Y-%m-%d")
                self.date_edit.setDate(QDate(d.year, d.month, d.day))
            except Exception:
                pass

        # Delivery
        sp = record.get("delivery_type", DELIVERY_TYPES[0])
        idx = self.sp_combo.findText(sp)
        if idx >= 0:
            self.sp_combo.setCurrentIndex(idx)

        # Suffix
        self.suffix_edit.setText(record.get("ref_suffix", ""))

        # Text fields
        self.to_field.setText(record.get("to_field", ""))
        self.designation.setText(record.get("designation", ""))
        self.designation_hi.setText(record.get("designation_hi", ""))
        self.office_name.setText(record.get("office_name", ""))
        self.addr_line1.setText(record.get("addr_line1", ""))
        self.addr_line2.setText(record.get("addr_line2", ""))
        self.city.setText(record.get("city", ""))
        self.state.setText(record.get("state", ""))
        self.pin_code.setText(record.get("pin_code", ""))
        self.email.setText(record.get("email", ""))
        self.fax.setText(record.get("fax", ""))
        self.contact_no.setText(record.get("contact_no", ""))

        self._update_envelope_preview()

    def _collect_data(self) -> dict | None:
        """Validate and collect form data. Returns None if validation fails."""
        errors = []
        data = {}

        # Required fields
        required_map = {
            "designation": self.designation.text().strip(),
            "office_name": self.office_name.text().strip(),
            "addr_line1":  self.addr_line1.text().strip(),
            "city":        self.city.text().strip(),
            "state":       self.state.text().strip(),
            "pin_code":    self.pin_code.text().strip(),
        }
        for key, val in required_map.items():
            if not val:
                errors.append(f"Field '{key}' is required.")
            else:
                data[key] = val

        # PIN validation
        if data.get("pin_code") and not validate_pin_code(data["pin_code"]):
            errors.append("PIN code must be 6 digits. / पिन कोड 6 अंकों का होना चाहिए।")

        # Email validation
        email = self.email.text().strip()
        if email and not validate_email(email):
            errors.append("Invalid email format. / अमान्य ईमेल प्रारूप।")

        if errors:
            show_error(self, "Validation Error / मान्यता त्रुटि",
                       "\n".join(errors))
            return None

        # Dept
        dept_label = self.dept_combo.currentText()
        data["dept_id"] = self._dept_map.get(dept_label)
        data["designation_hi"]  = self.designation_hi.text().strip()
        data["to_field"]        = self.to_field.text().strip()
        data["addr_line2"]      = self.addr_line2.text().strip()
        data["email"]           = email
        data["fax"]             = self.fax.text().strip()
        data["contact_no"]      = self.contact_no.text().strip()
        data["para_no"]         = self.para_combo.currentText()
        data["date_entry"]      = self.date_edit.date().toString("yyyy-MM-dd")
        data["delivery_type"]   = self.sp_combo.currentText()
        data["ref_suffix"]      = self.suffix_edit.toPlainText().strip()

        return data

    def _save(self):
        data = self._collect_data()
        if data is None:
            return

        office_name_text = data.get("office_name", "").strip()
        if office_name_text:
            from modules.department_ops import get_all_departments, add_department
            depts = get_all_departments()
            exists = False
            for d in depts:
                if d["dept_name"].strip().lower() == office_name_text.lower():
                    exists = True
                    if not data.get("dept_id"):
                        data["dept_id"] = d["dept_id"]
                    break
            
            if not exists:
                ok, msg = add_department(office_name_text, "")
                if ok:
                    depts = get_all_departments()
                    for d in depts:
                        if d["dept_name"].strip().lower() == office_name_text.lower():
                            if not data.get("dept_id"):
                                data["dept_id"] = d["dept_id"]
                            break
                    self._load_departments()
                    
        if not data.get("dept_id"):
            show_error(self, "Validation Error / त्रुटि", "Please select a Department or enter a valid Office/Dept Name.")
            return

        if self.mode == "add":
            ok, msg = add_address(data)
        else:
            ok, msg = update_address(self.record["id"], data)

        if ok:
            show_info(self, "Success / सफलता", msg)
            self.saved.emit()
        else:
            show_error(self, "Error / त्रुटि", msg)

    def _clear(self):
        for w in [self.to_field, self.designation, self.designation_hi,
                  self.office_name, self.addr_line1, self.addr_line2,
                  self.city, self.state, self.pin_code,
                  self.email, self.fax, self.contact_no]:
            w.clear()
        self.suffix_edit.clear()
        self.para_combo.setCurrentIndex(0)
        self.date_edit.setDate(QDate.currentDate())
        self.sp_combo.setCurrentIndex(0)
        self._update_envelope_preview()

    def _set_readonly(self, ro: bool):
        for w in [self.to_field, self.designation, self.designation_hi,
                  self.office_name, self.addr_line1, self.addr_line2,
                  self.city, self.state, self.pin_code,
                  self.email, self.fax, self.contact_no]:
            w.setReadOnly(ro)
        self.suffix_edit.setReadOnly(ro)
        self.para_combo.setEnabled(not ro)
        self.date_edit.setEnabled(not ro)
        self.sp_combo.setEnabled(not ro)
        self.dept_combo.setEnabled(not ro)

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

    def _print_single(self):
        rec = {
            "para_no": self.para_combo.currentText(),
            "date_entry": self.date_edit.date().toString("yyyy-MM-dd"),
            "ref_suffix": self.suffix_edit.toPlainText().strip(),
            "delivery_type": self.sp_combo.currentText(),
            "to_field": self.to_field.text().strip(),
            "designation": self.designation.text().strip(),
            "office_name": self.office_name.text().strip(),
            "addr_line1": self.addr_line1.text().strip(),
            "addr_line2": self.addr_line2.text().strip(),
            "city": self.city.text().strip(),
            "state": self.state.text().strip(),
            "pin_code": self.pin_code.text().strip(),
        }
        
        from modules.export_action import execute_export_action
        from modules.print_module import generate_single_envelope_pdf
        execute_export_action(
            parent_widget=self,
            records=[rec],
            pdf_suffix="Envelope",
            pdf_generator_func=lambda path: generate_single_envelope_pdf(rec, path),
            is_envelope_or_label=True
        )

    def _open_envelope_preview_dialog(self):
        html = self._get_preview_html(is_dialog=True)

        dialog = QDialog(self)
        dialog.setWindowTitle("Envelope Preview / लिफाफा पूर्वावलोकन")
        dialog.resize(850, 480)
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        preview_text = QTextEdit()
        preview_text.setReadOnly(True)
        preview_text.setHtml(html)
        
        preview_text.setStyleSheet("""
            QTextEdit {
                background-color: #FAFAFA;
                color: #000000;
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                padding: 20px;
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
