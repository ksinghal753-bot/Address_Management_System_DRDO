"""
Address View / Search / Print Screen.
Available to both Admin (with edit/delete) and User (view/print only).
"""

import os
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QGroupBox, QSplitter, QTextEdit, QFrame,
    QAbstractItemView, QFileDialog, QSizePolicy, QCheckBox
)
from PySide6.QtCore import Qt, Signal, QDate, QSize
from PySide6.QtGui import QFont, QColor

from modules.address_ops import (
    get_all_addresses, search_addresses, delete_address, get_address_stats
)
from modules.department_ops import get_all_departments
from modules.print_module import (
    generate_single_envelope_pdf, generate_department_list_pdf,
    generate_full_directory_pdf, open_pdf, get_default_output_dir,
    format_ref_no
)
from ui.shared_widgets import (
    HeaderBar, SectionTitle, HLine, show_error, show_info,
    show_warning, show_question
)
from utils.constants import COLORS, LABELS, PARA_OPTIONS, DELIVERY_TYPES, ENVELOPE_PREFIX


TABLE_COLUMNS = [
    ("ID", "id"),
    ("Dept / αñ╡αñ┐αñ¡αñ╛αñù", "dept_name"),
    ("To / αñ╕αÑçαñ╡αñ╛ αñ«αÑçαñé", "to_field"),
    ("Designation / αñ¬αñªαñ¿αñ╛αñ«", "designation"),
    ("Office / αñòαñ╛αñ░αÑìαñ»αñ╛αñ▓αñ»", "office_name"),
    ("City / αñ╢αñ╣αñ░", "city"),
    ("State / αñ░αñ╛αñ£αÑìαñ»", "state"),
    ("PIN", "pin_code"),
    ("PARA / αñ¬αÑêαñ░αñ╛", "para_no"),
    ("Date / αñªαñ┐αñ¿αñ╛αñéαñò", "date_entry"),
    ("By S/P", "delivery_type"),
]


class AddressView(QWidget):
    """
    Combined search + table + envelope preview + print panel.
    role: 'admin' | 'user'
    Emits: go_back(), edit_record(dict), add_new()
    """
    go_back     = Signal()
    edit_record = Signal(dict)
    add_new     = Signal()

    def __init__(self, role: str = "user", parent=None):
        super().__init__(parent)
        self.role = role
        self._records: list[dict] = []
        self._selected_record: dict | None = None
        self._build_ui()
        self._load_records()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)



        # ΓöÇΓöÇ Toolbar ΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇ
        toolbar = QWidget()
        toolbar.setStyleSheet(f"background: {COLORS['primary_dark']}; padding: 4px 12px;")
        tl = QHBoxLayout(toolbar)
        tl.setContentsMargins(10, 6, 10, 6)
        tl.setSpacing(10)

        title = QLabel("≡ƒôï  Address Records / αñ¬αññαñ╛ αñàαñ¡αñ┐αñ▓αÑçαñû")
        title.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        tl.addWidget(title)
        tl.addStretch()

        # Stats label
        self.stats_lbl = QLabel("")
        self.stats_lbl.setStyleSheet(f"color: {COLORS['accent_light']}; font-size: 12px;")
        tl.addWidget(self.stats_lbl)

        if self.role == "admin":
            self.add_btn = QPushButton("Γ₧ò " + LABELS["add"])
            self.add_btn.setObjectName("successButton")
            self.add_btn.clicked.connect(self.add_new.emit)
            tl.addWidget(self.add_btn)

        back_btn = QPushButton("ΓåÉ " + LABELS["return"])
        back_btn.clicked.connect(self.go_back.emit)
        tl.addWidget(back_btn)

        root.addWidget(toolbar)

        # ΓöÇΓöÇ Main splitter ΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇ
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(4)

        # Left: search + table
        left_widget = QWidget()
        left_widget.setObjectName("addressViewLeft")
        left_widget.setStyleSheet(f"#addressViewLeft {{ background-color: {COLORS['surface']}; }}")
        left_vbox = QVBoxLayout(left_widget)
        left_vbox.setContentsMargins(12, 12, 6, 12)
        left_vbox.setSpacing(10)

        # Search panel
        search_group = QGroupBox("Search / αñûαÑïαñ£αÑçαñé")
        sg = QVBoxLayout(search_group)
        sg.setSpacing(8)

        row1 = QHBoxLayout()
        # Department filter
        dept_lbl = QLabel("Dept:")
        dept_lbl.setObjectName("fieldLabel")
        self.dept_filter = QComboBox()
        self.dept_filter.setMinimumWidth(160)
        self._load_dept_filter()

        # PARA filter
        para_lbl = QLabel("PARA:")
        para_lbl.setObjectName("fieldLabel")
        self.para_filter = QComboBox()
        self.para_filter.addItem("All / αñ╕αñ¡αÑÇ", None)
        for p in PARA_OPTIONS:
            self.para_filter.addItem(p)

        row1.addWidget(dept_lbl)
        row1.addWidget(self.dept_filter)
        row1.addSpacing(10)
        row1.addWidget(para_lbl)
        row1.addWidget(self.para_filter)
        row1.addStretch()

        row2 = QHBoxLayout()
        # Keyword search
        kw_lbl = QLabel("Keyword:")
        kw_lbl.setObjectName("fieldLabel")
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("Office, City, Name... / αñòαñ╛αñ░αÑìαñ»αñ╛αñ▓αñ», αñ╢αñ╣αñ░, αñ¿αñ╛αñ«...")
        self.keyword_input.setMinimumWidth(200)
        self.keyword_input.returnPressed.connect(self._do_search)

        # City filter
        city_lbl = QLabel("City / PIN:")
        city_lbl.setObjectName("fieldLabel")
        self.city_filter = QLineEdit()
        self.city_filter.setPlaceholderText("City or PIN")
        self.city_filter.setMaximumWidth(120)

        # Date filter
        date_lbl = QLabel("Date:")
        date_lbl.setObjectName("fieldLabel")
        self.use_date = QCheckBox()
        self.date_filter = QDateEdit()
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.setDisplayFormat("dd-MM-yyyy")
        self.date_filter.setEnabled(False)
        self.use_date.toggled.connect(self.date_filter.setEnabled)

        row2.addWidget(kw_lbl)
        row2.addWidget(self.keyword_input)
        row2.addSpacing(8)
        row2.addWidget(city_lbl)
        row2.addWidget(self.city_filter)
        row2.addSpacing(8)
        row2.addWidget(date_lbl)
        row2.addWidget(self.use_date)
        row2.addWidget(self.date_filter)
        row2.addStretch()

        btn_row = QHBoxLayout()
        search_btn = QPushButton("≡ƒöì " + LABELS["search"])
        search_btn.clicked.connect(self._do_search)
        clear_btn = QPushButton("Γ£û Clear / αñ╕αñ╛αñ½")
        clear_btn.clicked.connect(self._clear_search)
        btn_row.addWidget(search_btn)
        btn_row.addWidget(clear_btn)
        btn_row.addStretch()

        sg.addLayout(row1)
        sg.addLayout(row2)
        sg.addLayout(btn_row)
        left_vbox.addWidget(search_group)

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
        self.table.setSortingEnabled(True)
        self.table.itemSelectionChanged.connect(self._on_row_selected)
        self.table.doubleClicked.connect(self._on_row_double_clicked)

        # Hide ID column
        self.table.setColumnHidden(0, True)

        left_vbox.addWidget(self.table, stretch=1)

        # Record action buttons (below table)
        action_row = QHBoxLayout()
        self.view_btn = QPushButton("≡ƒæü∩╕Å View / αñªαÑçαñûαÑçαñé")
        self.view_btn.setEnabled(False)
        self.view_btn.clicked.connect(self._view_selected)

        self.print_btn = QPushButton("≡ƒû¿∩╕Å " + LABELS["print"])
        self.print_btn.setEnabled(False)
        self.print_btn.clicked.connect(self._print_single)

        self.print_all_btn = QPushButton("≡ƒôä Print All / αñ╕αñ¡αÑÇ αñ¬αÑìαñ░αñ┐αñéαñƒ")
        self.print_all_btn.clicked.connect(self._print_all)

        self.print_dept_btn = QPushButton("≡ƒôï Print Dept / αñ╡αñ┐αñ¡αñ╛αñù αñ¬αÑìαñ░αñ┐αñéαñƒ")
        self.print_dept_btn.clicked.connect(self._print_dept)

        action_row.addWidget(self.view_btn)
        action_row.addWidget(self.print_btn)
        action_row.addWidget(self.print_dept_btn)
        action_row.addWidget(self.print_all_btn)

        if self.role == "admin":
            self.edit_btn = QPushButton("Γ£Å∩╕Å " + LABELS["edit"])
            self.edit_btn.setEnabled(False)
            self.edit_btn.clicked.connect(self._edit_selected)

            self.del_btn = QPushButton("≡ƒùæ∩╕Å " + LABELS["delete"])
            self.del_btn.setObjectName("dangerButton")
            self.del_btn.setEnabled(False)
            self.del_btn.clicked.connect(self._delete_selected)

            action_row.addWidget(self.edit_btn)
            action_row.addWidget(self.del_btn)

        left_vbox.addLayout(action_row)
        splitter.addWidget(left_widget)

        # Right: envelope preview
        right_widget = QWidget()
        right_widget.setObjectName("addressViewRight")
        right_widget.setStyleSheet(f"#addressViewRight {{ background-color: {COLORS['surface']}; }}")
        right_vbox = QVBoxLayout(right_widget)
        right_vbox.setContentsMargins(6, 12, 12, 12)
        right_vbox.setSpacing(8)

        prev_title = SectionTitle("Envelope Preview / αñ▓αñ┐αñ½αñ╛αñ½αñ╛ αñ¬αÑéαñ░αÑìαñ╡αñ╛αñ╡αñ▓αÑïαñòαñ¿")
        right_vbox.addWidget(prev_title)
        right_vbox.addWidget(HLine())

        self.envelope_preview = QTextEdit()
        self.envelope_preview.setReadOnly(True)
        self.envelope_preview.setObjectName("envelopePreview")
        self.envelope_preview.setFont(QFont("Courier New", 11))
        right_vbox.addWidget(self.envelope_preview, stretch=1)

        # SP selector in preview panel
        sp_row = QHBoxLayout()
        sp_lbl = QLabel("By S/P / αñíαñ╛αñò αñ¬αÑìαñ░αñòαñ╛αñ░:")
        sp_lbl.setObjectName("fieldLabel")
        self.preview_sp = QComboBox()
        self.preview_sp.addItems(DELIVERY_TYPES)
        self.preview_sp.currentIndexChanged.connect(self._update_preview)
        sp_row.addWidget(sp_lbl)
        sp_row.addWidget(self.preview_sp)
        sp_row.addStretch()
        right_vbox.addLayout(sp_row)

        # Date picker for print
        date_row = QHBoxLayout()
        date_print_lbl = QLabel("Print Date / αñ¬αÑìαñ░αñ┐αñéαñƒ αñªαñ┐αñ¿αñ╛αñéαñò:")
        date_print_lbl.setObjectName("fieldLabel")
        self.preview_date = QDateEdit()
        self.preview_date.setCalendarPopup(True)
        self.preview_date.setDate(QDate.currentDate())
        self.preview_date.setDisplayFormat("dd-MM-yyyy")
        self.preview_date.dateChanged.connect(self._update_preview)
        date_row.addWidget(date_print_lbl)
        date_row.addWidget(self.preview_date)
        date_row.addStretch()
        right_vbox.addLayout(date_row)

        splitter.addWidget(right_widget)
        splitter.setSizes([700, 380])

        root.addWidget(splitter, stretch=1)

    def _load_dept_filter(self):
        self.dept_filter.clear()
        self.dept_filter.addItem("All Departments / αñ╕αñ¡αÑÇ αñ╡αñ┐αñ¡αñ╛αñù", None)
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
                self.add_btn.setToolTip("Database Full (500/500) / αñíαÑçαñƒαñ╛αñ¼αÑçαñ╕ αñ¬αÑéαñ░αÑìαñú (500/500)")
            else:
                self.add_btn.setToolTip("Add new address record / αñ¿αñ»αñ╛ αñ¬αññαñ╛ αñ░αñ┐αñòαÑëαñ░αÑìαñí αñ£αÑïαñíαñ╝αÑçαñé")

    def _populate_table(self, records: list):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        for row_idx, rec in enumerate(records):
            self.table.insertRow(row_idx)
            for col_idx, (_, key) in enumerate(TABLE_COLUMNS):
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
                item.setData(Qt.UserRole, rec)
                self.table.setItem(row_idx, col_idx, item)
        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)

    def _do_search(self):
        dept_id = self.dept_filter.currentData()
        para    = self.para_filter.currentText()
        para    = para if para != "All / αñ╕αñ¡αÑÇ" else ""
        keyword = self.keyword_input.text().strip()
        city_pin = self.city_filter.text().strip()
        date_str = ""
        if self.use_date.isChecked():
            date_str = self.date_filter.date().toString("yyyy-MM-dd")

        city = city_pin if not city_pin.isdigit() else ""
        pin  = city_pin if city_pin.isdigit() else ""

        results = search_addresses(
            dept_id=dept_id,
            para_no=para,
            keyword=keyword,
            city=city,
            pin_code=pin,
            date_entry=date_str
        )
        self._load_records(results)

    def _clear_search(self):
        self.dept_filter.setCurrentIndex(0)
        self.para_filter.setCurrentIndex(0)
        self.keyword_input.clear()
        self.city_filter.clear()
        self.use_date.setChecked(False)
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

    def _on_row_double_clicked(self):
        self._view_selected()

    def _set_action_btns(self, enabled: bool):
        self.view_btn.setEnabled(enabled)
        self.print_btn.setEnabled(enabled)
        if self.role == "admin":
            self.edit_btn.setEnabled(enabled)
            self.del_btn.setEnabled(enabled)

    def _update_preview(self):
        if not self._selected_record:
            self.envelope_preview.setPlainText(
                "ΓåÉ Select a record to preview the envelope.\nΓåÉ αñ¬αññαñ╛ αñªαÑçαñûαñ¿αÑç αñòαÑç αñ▓αñ┐αñÅ αñ░αñ┐αñòαÑëαñ░αÑìαñí αñÜαÑüαñ¿αÑçαñéαÑñ"
            )
            return
        rec = self._selected_record.copy()
        # Override SP and date from preview panel
        rec["delivery_type"] = self.preview_sp.currentText()
        rec["date_entry"]    = self.preview_date.date().toString("yyyy-MM-dd")

        ref = format_ref_no(rec.get("para_no", ""), rec.get("date_entry", ""))
        sp  = rec.get("delivery_type", "Ordinary / αñ╕αñ╛αñºαñ╛αñ░αñú")

        lines = [
            f"                    {ref}",
            "",
            "To,",
            rec.get("to_field", ""),
            rec.get("designation", ""),
            rec.get("office_name", ""),
            rec.get("addr_line1", ""),
        ]
        if rec.get("addr_line2"):
            lines.append(rec["addr_line2"])
        city_state = ", ".join(filter(None, [rec.get("city",""), rec.get("state","")]))
        if city_state:
            lines.append(city_state)
        if rec.get("pin_code"):
            lines.append(f"PIN Code: {rec['pin_code']}")
        lines += ["", f"                    By S/P: {sp}"]

        self.envelope_preview.setPlainText("\n".join(lines))

    def _view_selected(self):
        if not self._selected_record:
            return
        from ui.address_form import AddressForm
        form = AddressForm(mode="view", record=self._selected_record)
        form.cancelled.connect(form.close)
        form.setWindowFlags(Qt.Window)
        form.resize(850, 700)
        form.setWindowTitle("View Address / αñ¬αññαñ╛ αñªαÑçαñûαÑçαñé")
        form.show()

    def _edit_selected(self):
        if not self._selected_record:
            return
        self.edit_record.emit(self._selected_record)

    def _delete_selected(self):
        if not self._selected_record:
            return
        rec = self._selected_record
        if show_question(
            self,
            "Confirm Delete / αñ╣αñƒαñ╛αñ¿αÑç αñòαÑÇ αñ¬αÑüαñ╖αÑìαñƒαñ┐",
            f"Are you sure you want to delete this record?\n"
            f"αñòαÑìαñ»αñ╛ αñåαñ¬ αñçαñ╕ αñ░αñ┐αñòαÑëαñ░αÑìαñí αñòαÑï αñ╣αñƒαñ╛αñ¿αñ╛ αñÜαñ╛αñ╣αññαÑç αñ╣αÑêαñé?\n\n"
            f"Office: {rec.get('office_name','')}\n"
            f"City: {rec.get('city','')}"
        ):
            ok, msg = delete_address(rec["id"])
            if ok:
                show_info(self, "Deleted / αñ╣αñƒαñ╛αñ»αñ╛ αñùαñ»αñ╛", msg)
                self._load_records()
                self._selected_record = None
                self._update_preview()
            else:
                show_error(self, "Error / αññαÑìαñ░αÑüαñƒαñ┐", msg)

    def _get_print_path(self, suffix: str) -> str | None:
        out_dir = get_default_output_dir()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = os.path.join(out_dir, f"ADRDE_{suffix}_{ts}.pdf")
        path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF / PDF αñ╕αñ╣αÑçαñ£αÑçαñé",
            default_name,
            "PDF Files (*.pdf)"
        )
        return path if path else None

    def _get_record_for_print(self) -> dict:
        """Get selected record with preview panel overrides applied."""
        rec = self._selected_record.copy()
        rec["delivery_type"] = self.preview_sp.currentText()
        rec["date_entry"]    = self.preview_date.date().toString("yyyy-MM-dd")
        return rec

    def _print_single(self):
        if not self._selected_record:
            return
        path = self._get_print_path("Envelope")
        if not path:
            return
        rec = self._get_record_for_print()
        ok, result = generate_single_envelope_pdf(rec, path)
        if ok:
            show_info(self, "PDF Generated / PDF αñ¼αñ¿αñ╛", LABELS["print_success"])
            open_pdf(path)
        else:
            show_error(self, "Print Error / αñ¬αÑìαñ░αñ┐αñéαñƒ αññαÑìαñ░αÑüαñƒαñ┐", result)

    def _print_dept(self):
        dept_id = self.dept_filter.currentData()
        dept_name = self.dept_filter.currentText()
        if not dept_id:
            show_warning(self, "Select Department / αñ╡αñ┐αñ¡αñ╛αñù αñÜαÑüαñ¿αÑçαñé",
                         "Please select a specific department first.\nαñòαÑâαñ¬αñ»αñ╛ αñ¬αñ╣αñ▓αÑç αñÅαñò αñ╡αñ┐αñ¡αñ╛αñù αñÜαÑüαñ¿αÑçαñéαÑñ")
            return
        records = get_all_addresses(dept_id=dept_id)
        if not records:
            show_info(self, "No Records", LABELS["no_records"])
            return
        path = self._get_print_path(f"Dept_{dept_name.split('(')[0].strip()}")
        if not path:
            return
        ok, result = generate_department_list_pdf(records, dept_name, path)
        if ok:
            show_info(self, "PDF Generated / PDF αñ¼αñ¿αñ╛", LABELS["print_success"])
            open_pdf(path)
        else:
            show_error(self, "Print Error / αñ¬αÑìαñ░αñ┐αñéαñƒ αññαÑìαñ░αÑüαñƒαñ┐", result)

    def _print_all(self):
        records = get_all_addresses()
        if not records:
            show_info(self, "No Records", LABELS["no_records"])
            return
        path = self._get_print_path("FullDirectory")
        if not path:
            return
        ok, result = generate_full_directory_pdf(records, path)
        if ok:
            show_info(self, "PDF Generated / PDF αñ¼αñ¿αñ╛", LABELS["print_success"])
            open_pdf(path)
        else:
            show_error(self, "Print Error / αñ¬αÑìαñ░αñ┐αñéαñƒ αññαÑìαñ░αÑüαñƒαñ┐", result)

    def refresh(self):
        """Reload all records from DB."""
        self._load_records()
