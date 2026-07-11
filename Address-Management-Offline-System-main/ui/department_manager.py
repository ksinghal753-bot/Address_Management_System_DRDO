"""
Department Manager — Admin only.
Add, edit, delete departments.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QGroupBox, QFormLayout, QAbstractItemView, QDialog,
    QDialogButtonBox, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from modules.department_ops import (
    get_all_departments, add_department, update_department, delete_department
)
from ui.shared_widgets import (
    HeaderBar, SectionTitle, HLine, show_error, show_info, show_question
)
from utils.constants import COLORS, LABELS


class DepartmentManager(QWidget):
    """Department CRUD screen — Admin only."""
    go_back = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selected_dept: dict | None = None
        self._build_ui()
        self._load_departments()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)



        # Toolbar
        toolbar = QWidget()
        toolbar.setStyleSheet(f"background: {COLORS['primary_dark']}; padding: 4px 12px;")
        tl = QHBoxLayout(toolbar)
        tl.setContentsMargins(10, 6, 10, 6)
        title = QLabel("🏢  Manage Departments / विभाग प्रबंधन")
        title.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        tl.addWidget(title)
        tl.addStretch()
        back_btn = QPushButton("← " + LABELS["return"])
        back_btn.clicked.connect(self.go_back.emit)
        tl.addWidget(back_btn)
        root.addWidget(toolbar)

        content = QWidget()
        content.setObjectName("deptManagerContent")
        content.setStyleSheet(f"#deptManagerContent {{ background-color: {COLORS['surface']}; }}")
        cl = QHBoxLayout(content)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.setSpacing(16)

        # ── Left: table ────────────────────────────────────────────────────────
        left = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Department Name", "Hindi Name"])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnHidden(0, True)
        self.table.itemSelectionChanged.connect(self._on_select)
        left.addWidget(self.table, stretch=1)

        # Action buttons
        btn_row = QHBoxLayout()
        self.edit_btn = QPushButton("✏️ Edit / संपादित")
        self.edit_btn.setEnabled(False)
        self.edit_btn.clicked.connect(self._edit)
        self.del_btn = QPushButton("🗑️ Delete / हटाएं")
        self.del_btn.setObjectName("dangerButton")
        self.del_btn.setEnabled(False)
        self.del_btn.clicked.connect(self._delete)
        btn_row.addWidget(self.edit_btn)
        btn_row.addWidget(self.del_btn)
        btn_row.addStretch()
        left.addLayout(btn_row)

        cl.addLayout(left, stretch=2)

        # ── Right: add/edit form ──────────────────────────────────────────────
        right_group = QGroupBox("Add Department / विभाग जोड़ें")
        right_group.setStyleSheet(
            f"QGroupBox {{ font-size: 13px; font-weight: bold; color: {COLORS['primary']}; }}"
        )
        form_layout = QVBoxLayout(right_group)
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(16, 20, 16, 16)

        name_lbl = QLabel("Department Name (English) / विभाग नाम (अंग्रेजी) *")
        name_lbl.setObjectName("fieldLabel")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. ADRDE")
        self.name_input.setMinimumHeight(38)

        hindi_lbl = QLabel("Department Name (Hindi) / विभाग नाम (हिंदी) *")
        hindi_lbl.setObjectName("fieldLabel")
        self.hindi_input = QLineEdit()
        self.hindi_input.setPlaceholderText("e.g. एडीआरडीई")
        self.hindi_input.setMinimumHeight(38)

        self.msg_lbl = QLabel("")
        self.msg_lbl.setWordWrap(True)
        self.msg_lbl.setStyleSheet(f"color: {COLORS['error']}; font-size: 11px;")

        self.save_btn = QPushButton("💾 Save Department / विभाग सहेजें")
        self.save_btn.setObjectName("successButton")
        self.save_btn.setMinimumHeight(42)
        self.save_btn.clicked.connect(self._save)

        self.clear_btn = QPushButton("✖ Clear / साफ")
        self.clear_btn.clicked.connect(self._clear_form)

        form_layout.addWidget(name_lbl)
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(hindi_lbl)
        form_layout.addWidget(self.hindi_input)
        form_layout.addWidget(self.msg_lbl)
        form_layout.addWidget(self.save_btn)
        form_layout.addWidget(self.clear_btn)
        form_layout.addStretch()

        cl.addWidget(right_group, stretch=1)
        root.addWidget(content, stretch=1)

        self._editing_id: int | None = None

    def _load_departments(self):
        depts = get_all_departments()
        self.table.setRowCount(0)
        for i, d in enumerate(depts):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(d["dept_id"])))
            self.table.setItem(i, 1, QTableWidgetItem(d["dept_name"]))
            self.table.setItem(i, 2, QTableWidgetItem(d["dept_name_hindi"]))
            for col in range(3):
                item = self.table.item(i, col)
                if item:
                    item.setData(Qt.UserRole, d)
        self.table.resizeColumnsToContents()

    def _on_select(self):
        rows = self.table.selectedItems()
        enabled = bool(rows)
        self.edit_btn.setEnabled(enabled)
        self.del_btn.setEnabled(enabled)
        if rows:
            self._selected_dept = self.table.item(rows[0].row(), 0).data(Qt.UserRole)

    def _save(self):
        name  = self.name_input.text().strip()
        hindi = self.hindi_input.text().strip()
        if not name or not hindi:
            self.msg_lbl.setText("Both fields are required. / दोनों फ़ील्ड आवश्यक हैं।")
            return
        self.msg_lbl.clear()

        if self._editing_id:
            ok, msg = update_department(self._editing_id, name, hindi)
        else:
            ok, msg = add_department(name, hindi)

        if ok:
            show_info(self, "Success / सफलता", msg)
            self._clear_form()
            self._load_departments()
        else:
            self.msg_lbl.setText(msg)

    def _edit(self):
        if not self._selected_dept:
            return
        self._editing_id = self._selected_dept["dept_id"]
        self.name_input.setText(self._selected_dept["dept_name"])
        self.hindi_input.setText(self._selected_dept["dept_name_hindi"])
        self.save_btn.setText("💾 Update Department / विभाग अपडेट करें")

    def _delete(self):
        if not self._selected_dept:
            return
        if show_question(
            self, "Confirm Delete / हटाने की पुष्टि",
            f"Delete department '{self._selected_dept['dept_name']}'?\n"
            f"विभाग '{self._selected_dept['dept_name_hindi']}' हटाएं?"
        ):
            ok, msg = delete_department(self._selected_dept["dept_id"])
            if ok:
                show_info(self, "Deleted", msg)
                self._load_departments()
            else:
                show_error(self, "Error", msg)

    def _clear_form(self):
        self._editing_id = None
        self.name_input.clear()
        self.hindi_input.clear()
        self.msg_lbl.clear()
        self.save_btn.setText("💾 Save Department / विभाग सहेजें")
