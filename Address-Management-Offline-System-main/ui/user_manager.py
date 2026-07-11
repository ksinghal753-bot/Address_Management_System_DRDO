"""
User Manager — Admin only.
Add, edit, delete, unlock users and reset passwords.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QGroupBox, QComboBox, QStyleFactory, QListView, QCalendarWidget, QAbstractItemView, QCheckBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor

from modules.department_ops import (
    get_all_users, add_user, update_user, delete_user,
    unlock_user, reset_password
)
from ui.shared_widgets import (
    HeaderBar, SectionTitle, HLine, show_error, show_info,
    show_warning, show_question
)
from utils.constants import COLORS, LABELS
from utils.validators import validate_username, validate_password


class UserManager(QWidget):
    """User management screen — Admin only."""
    go_back = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selected_user: dict | None = None
        self._editing_id: int | None = None
        self._build_ui()
        self._load_users()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)



        # Toolbar
        toolbar = QWidget()
        toolbar.setStyleSheet(f"background: {COLORS['primary_dark']}; padding: 4px 12px;")
        tl = QHBoxLayout(toolbar)
        tl.setContentsMargins(10, 6, 10, 6)
        title = QLabel("👥  Manage Users / उपयोगकर्ता प्रबंधन")
        title.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        tl.addWidget(title)
        tl.addStretch()
        back_btn = QPushButton("← " + LABELS["return"])
        back_btn.clicked.connect(self.go_back.emit)
        tl.addWidget(back_btn)
        root.addWidget(toolbar)

        content = QWidget()
        content.setObjectName("userManagerContent")
        content.setStyleSheet(f"#userManagerContent {{ background-color: {COLORS['surface']}; }}")
        cl = QHBoxLayout(content)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.setSpacing(16)

        # ── Left: user table ──────────────────────────────────────────────────
        left = QVBoxLayout()
        cols = ["ID", "Username", "Role", "Status", "Failed Attempts", "Last Login"]
        self.table = QTableWidget()
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnHidden(0, True)
        self.table.itemSelectionChanged.connect(self._on_select)
        left.addWidget(self.table, stretch=1)

        btn_row = QHBoxLayout()
        self.edit_btn   = QPushButton("✏️ Edit / संपादित")
        self.edit_btn.setEnabled(False)
        self.edit_btn.clicked.connect(self._load_for_edit)

        self.unlock_btn = QPushButton("🔓 Unlock / अनलॉक")
        self.unlock_btn.setEnabled(False)
        self.unlock_btn.clicked.connect(self._unlock)

        self.reset_btn  = QPushButton("🔑 Reset PW / पासवर्ड रीसेट")
        self.reset_btn.setEnabled(False)
        self.reset_btn.clicked.connect(self._reset_password_dialog)

        self.del_btn = QPushButton("🗑️ Delete / हटाएं")
        self.del_btn.setObjectName("dangerButton")
        self.del_btn.setEnabled(False)
        self.del_btn.clicked.connect(self._delete)

        btn_row.addWidget(self.edit_btn)
        btn_row.addWidget(self.unlock_btn)
        btn_row.addWidget(self.reset_btn)
        btn_row.addWidget(self.del_btn)
        btn_row.addStretch()
        left.addLayout(btn_row)
        cl.addLayout(left, stretch=2)

        # ── Right: add/edit form ──────────────────────────────────────────────
        right_group = QGroupBox("Add / Edit User / उपयोगकर्ता जोड़ें / संपादित करें")
        fl = QVBoxLayout(right_group)
        fl.setSpacing(12)
        fl.setContentsMargins(16, 20, 16, 16)

        uname_lbl = QLabel("Username / उपयोगकर्ता नाम *")
        uname_lbl.setObjectName("fieldLabel")
        self.uname_input = QLineEdit()
        self.uname_input.setPlaceholderText("3-50 alphanumeric chars")
        self.uname_input.setMinimumHeight(38)

        role_lbl = QLabel("Role / भूमिका *")
        role_lbl.setObjectName("fieldLabel")
        self.role_combo = QComboBox()
        self.role_combo.setStyle(QStyleFactory.create('Fusion'))
        self.role_combo.setView(QListView())
        self.role_combo.addItems(["user", "admin"])
        self.role_combo.setMinimumHeight(38)

        pass_lbl = QLabel("Password / पासवर्ड")
        pass_lbl.setObjectName("fieldLabel")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setPlaceholderText("Leave blank to keep existing (edit mode)")
        self.pass_input.setMinimumHeight(38)

        pass_note = QLabel("Min 8 chars, 1 uppercase, 1 digit\nकम से कम 8 अक्षर, 1 बड़ा अक्षर, 1 अंक")
        pass_note.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")

        self.msg_lbl = QLabel("")
        self.msg_lbl.setWordWrap(True)
        self.msg_lbl.setStyleSheet(f"color: {COLORS['error']}; font-size: 11px;")

        self.save_btn = QPushButton("💾 Save User / उपयोगकर्ता सहेजें")
        self.save_btn.setObjectName("successButton")
        self.save_btn.setMinimumHeight(42)
        self.save_btn.clicked.connect(self._save)

        self.clear_btn = QPushButton("✖ Clear / साफ")
        self.clear_btn.clicked.connect(self._clear_form)

        fl.addWidget(uname_lbl)
        fl.addWidget(self.uname_input)
        fl.addWidget(role_lbl)
        fl.addWidget(self.role_combo)
        fl.addWidget(pass_lbl)
        fl.addWidget(self.pass_input)
        fl.addWidget(pass_note)
        fl.addWidget(self.msg_lbl)
        fl.addWidget(self.save_btn)
        fl.addWidget(self.clear_btn)
        fl.addStretch()

        cl.addWidget(right_group, stretch=1)
        root.addWidget(content, stretch=1)

    def _load_users(self):
        users = get_all_users()
        self.table.setRowCount(0)
        for i, u in enumerate(users):
            self.table.insertRow(i)
            status = "🔒 Locked" if u["is_locked"] else "✅ Active"
            last_login = u.get("last_login", "Never") or "Never"
            if last_login != "Never":
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(last_login)
                    last_login = dt.strftime("%d-%m-%Y %H:%M")
                except Exception:
                    pass

            values = [
                str(u["user_id"]), u["username"], u["role"],
                status, str(u["failed_attempts"]), last_login
            ]
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setData(Qt.UserRole, u)
                if u["is_locked"] and col == 3:
                    item.setForeground(QColor(COLORS["error"]))
                self.table.setItem(i, col, item)
        self.table.resizeColumnsToContents()

    def _on_select(self):
        rows = self.table.selectedItems()
        enabled = bool(rows)
        self.edit_btn.setEnabled(enabled)
        self.reset_btn.setEnabled(enabled)
        self.del_btn.setEnabled(enabled)
        if rows:
            user = self.table.item(rows[0].row(), 0).data(Qt.UserRole)
            self._selected_user = user
            self.unlock_btn.setEnabled(bool(user.get("is_locked")))

    def _load_for_edit(self):
        if not self._selected_user:
            return
        u = self._selected_user
        self._editing_id = u["user_id"]
        self.uname_input.setText(u["username"])
        idx = self.role_combo.findText(u["role"])
        if idx >= 0:
            self.role_combo.setCurrentIndex(idx)
        self.pass_input.clear()
        self.save_btn.setText("💾 Update User / उपयोगकर्ता अपडेट करें")

    def _save(self):
        username = self.uname_input.text().strip()
        role     = self.role_combo.currentText()
        password = self.pass_input.text()

        if not validate_username(username):
            self.msg_lbl.setText(
                "Invalid username. Use 3-50 letters/digits/underscore.\n"
                "अमान्य नाम। 3-50 अक्षर/अंक/अंडरस्कोर उपयोग करें।"
            )
            return

        if password:
            ok, pw_msg = validate_password(password)
            if not ok:
                self.msg_lbl.setText(pw_msg)
                return
        elif not self._editing_id:
            self.msg_lbl.setText("Password is required for new users.\nनए उपयोगकर्ता के लिए पासवर्ड आवश्यक है।")
            return

        self.msg_lbl.clear()

        if self._editing_id:
            ok, msg = update_user(self._editing_id, username, role, password)
        else:
            ok, msg = add_user(username, password, role)

        if ok:
            show_info(self, "Success / सफलता", msg)
            self._clear_form()
            self._load_users()
        else:
            self.msg_lbl.setText(msg)

    def _unlock(self):
        if not self._selected_user:
            return
        ok, msg = unlock_user(self._selected_user["user_id"])
        if ok:
            show_info(self, "Unlocked", msg)
            self._load_users()
        else:
            show_error(self, "Error", msg)

    def _delete(self):
        if not self._selected_user:
            return
        from modules.auth import current_session
        if self._selected_user["user_id"] == current_session.user_id:
            show_warning(self, "Cannot Delete",
                         "You cannot delete your own account.\nआप अपना खाता नहीं हटा सकते।")
            return
        if show_question(
            self, "Confirm Delete / हटाने की पुष्टि",
            f"Delete user '{self._selected_user['username']}'?\n"
            f"उपयोगकर्ता '{self._selected_user['username']}' हटाएं?"
        ):
            ok, msg = delete_user(self._selected_user["user_id"])
            if ok:
                show_info(self, "Deleted", msg)
                self._load_users()
            else:
                show_error(self, "Error", msg)

    def _clear_form(self):
        self._editing_id = None
        self.uname_input.clear()
        self.role_combo.setCurrentIndex(0)
        self.pass_input.clear()
        self.msg_lbl.clear()
        self.save_btn.setText("💾 Save User / उपयोगकर्ता सहेजें")

    def _reset_password_dialog(self):
        if not self._selected_user:
            return
        
        from PySide6.QtWidgets import QInputDialog, QLineEdit
        new_pass, ok = QInputDialog.getText(
            self,
            "Reset Password / पासवर्ड रीसेट",
            f"Enter new password for '{self._selected_user['username']}':\n"
            f"'{self._selected_user['username']}' के लिए नया पासवर्ड दर्ज करें:",
            QLineEdit.Password
        )
        if not ok or not new_pass:
            return
            
        pw_ok, pw_msg = validate_password(new_pass)
        if not pw_ok:
            show_error(self, "Invalid Password / अमान्य पासवर्ड", pw_msg)
            return
            
        success, msg = reset_password(self._selected_user["user_id"], new_pass)
        if success:
            show_info(self, "Success / सफलता", msg)
            self._load_users()
        else:
            show_error(self, "Error / त्रुटि", msg)
