"""
Settings Dialog — allows user to reset password and manage account.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QDialogButtonBox, QMessageBox, QLineEdit, QFormLayout
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from utils.constants import COLORS


class SettingsDialog(QDialog):
    theme_changed  = Signal(str)  # kept for compatibility
    account_deleted = Signal()    # Emitted when account is deleted

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings / सेटिंग्स")
        self.setMinimumWidth(440)
        self._build_ui()

    # ──────────────────────────────────────────────────────────────────
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)

        # ── Title ─────────────────────────────────────────────────────
        title = QLabel("⚙️ Application Settings / एप्लिकेशन सेटिंग्स")
        title.setStyleSheet(
            f"font-size: 18px; font-weight: bold; color: {COLORS['primary']};"
        )
        layout.addWidget(title)

        sep = self._hline()
        layout.addWidget(sep)

        # ── Reset Password Section ─────────────────────────────────────
        rp_title = QLabel("🔒 Reset Password / पासवर्ड बदलें")
        rp_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #1D4ED8;")
        layout.addWidget(rp_title)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        lbl_style = "font-weight: bold; color: #374151;"

        self.current_pw = QLineEdit()
        self.current_pw.setEchoMode(QLineEdit.Password)
        self.current_pw.setPlaceholderText("Enter current password")
        self.current_pw.setStyleSheet(self._input_style())
        form.addRow(self._lbl("Current Password / वर्तमान पासवर्ड:", lbl_style),
                    self.current_pw)

        self.new_pw = QLineEdit()
        self.new_pw.setEchoMode(QLineEdit.Password)
        self.new_pw.setPlaceholderText("Enter new password (min 6 chars)")
        self.new_pw.setStyleSheet(self._input_style())
        form.addRow(self._lbl("New Password / नया पासवर्ड:", lbl_style), self.new_pw)

        self.confirm_pw = QLineEdit()
        self.confirm_pw.setEchoMode(QLineEdit.Password)
        self.confirm_pw.setPlaceholderText("Confirm new password")
        self.confirm_pw.setStyleSheet(self._input_style())
        form.addRow(self._lbl("Confirm Password / पुष्टि करें:", lbl_style),
                    self.confirm_pw)

        layout.addLayout(form)

        # Reset Password button
        self.reset_btn = QPushButton("🔑  Change Password / पासवर्ड बदलें")
        self.reset_btn.setCursor(Qt.PointingHandCursor)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #1D4ED8;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover  { background-color: #1E40AF; }
            QPushButton:pressed { background-color: #1e3a8a; }
        """)
        self.reset_btn.clicked.connect(self._reset_password)
        layout.addWidget(self.reset_btn)

        # ── Danger Zone ────────────────────────────────────────────────
        layout.addWidget(self._hline())

        danger_layout = QHBoxLayout()
        danger_lbl = QLabel("Danger Zone / ख़तरे का क्षेत्र:")
        danger_lbl.setStyleSheet("font-weight: bold; color: #DC2626;")

        self.delete_acc_btn = QPushButton("🗑️ Delete Account / खाता हटाएं")
        self.delete_acc_btn.setCursor(Qt.PointingHandCursor)
        self.delete_acc_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC2626;
                color: #FFFFFF;
                border: 1px solid #B91C1C;
                border-radius: 8px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover  { background-color: #EF4444; }
            QPushButton:pressed { background-color: #B91C1C; }
        """)
        self.delete_acc_btn.clicked.connect(self._delete_account)

        danger_layout.addWidget(danger_lbl)
        danger_layout.addWidget(self.delete_acc_btn)
        layout.addLayout(danger_layout)

        layout.addStretch()

        # ── Dialog Buttons ─────────────────────────────────────────────
        btns = QDialogButtonBox(QDialogButtonBox.Cancel)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    # ──────────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────────
    def _hline(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet(f"background-color: {COLORS['border']};")
        return line

    def _lbl(self, text, style=""):
        lbl = QLabel(text)
        lbl.setStyleSheet(style)
        return lbl

    def _input_style(self):
        return (
            "QLineEdit {"
            "  background-color: #FFFFFF;"
            "  color: #212529;"
            "  border: 1.5px solid #D1D5DB;"
            "  border-radius: 6px;"
            "  padding: 6px 10px;"
            "  font-size: 13px;"
            "}"
            "QLineEdit:focus {"
            "  border: 1.5px solid #1D4ED8;"
            "}"
        )

    # ──────────────────────────────────────────────────────────────────
    # Actions
    # ──────────────────────────────────────────────────────────────────
    def _reset_password(self):
        import bcrypt
        from modules.auth import current_session, change_password
        from database.db_manager import db

        current = self.current_pw.text().strip()
        new     = self.new_pw.text().strip()
        confirm = self.confirm_pw.text().strip()

        if not current or not new or not confirm:
            QMessageBox.warning(self, "Missing Fields / खाली फ़ील्ड",
                                "Please fill in all password fields.\n"
                                "कृपया सभी पासवर्ड फ़ील्ड भरें।")
            return

        if new != confirm:
            QMessageBox.warning(self, "Mismatch / मेल नहीं",
                                "New password and confirmation do not match.\n"
                                "नया पासवर्ड और पुष्टि मेल नहीं खाते।")
            self.confirm_pw.clear()
            self.confirm_pw.setFocus()
            return

        if len(new) < 6:
            QMessageBox.warning(self, "Too Short / बहुत छोटा",
                                "Password must be at least 6 characters.\n"
                                "पासवर्ड कम से कम 6 अक्षर का होना चाहिए।")
            return

        # Verify current password against stored hash
        try:
            row = db.conn.execute(
                "SELECT password_hash FROM users WHERE user_id=?",
                (current_session.user_id,)
            ).fetchone()
            if not row or not bcrypt.checkpw(current.encode(), row["password_hash"].encode()):
                QMessageBox.critical(self, "Wrong Password / गलत पासवर्ड",
                                     "Current password is incorrect.\n"
                                     "वर्तमान पासवर्ड गलत है।")
                self.current_pw.clear()
                self.current_pw.setFocus()
                return
        except Exception as e:
            QMessageBox.critical(self, "Error / त्रुटि", str(e))
            return

        # Update password using bcrypt
        ok = change_password(current_session.user_id, new)
        if ok:
            QMessageBox.information(self, "Success / सफलता",
                                    "Password changed successfully!\n"
                                    "पासवर्ड सफलतापूर्वक बदल दिया गया है!")
            self.current_pw.clear()
            self.new_pw.clear()
            self.confirm_pw.clear()
            self.accept()
        else:
            QMessageBox.critical(self, "Error / त्रुटि",
                                 "Failed to change password. Please try again.\n"
                                 "पासवर्ड बदलने में विफल। कृपया पुनः प्रयास करें।")

    def _delete_account(self):
        from modules.auth import current_session, logout
        from modules.department_ops import delete_user

        if not current_session.is_authenticated:
            return

        reply = QMessageBox.question(
            self,
            "Delete Account / खाता हटाएं",
            "Are you sure you want to permanently delete your account?\n"
            "This action cannot be undone and you will be logged out.\n\n"
            "क्या आप निश्चित रूप से अपना खाता स्थायी रूप से हटाना चाहते हैं?\n"
            "यह क्रिया पूर्ववत नहीं की जा सकती है और आप लॉगआउट हो जाएंगे।",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            ok, msg = delete_user(current_session.user_id)
            if ok:
                QMessageBox.information(
                    self, "Account Deleted / खाता हटाया गया",
                    "Your account has been successfully deleted.\n"
                    "आपका खाता सफलतापूर्वक हटा दिया गया है।"
                )
                logout()
                self.account_deleted.emit()
                self.accept()
            else:
                QMessageBox.critical(
                    self, "Error / त्रुटि",
                    f"Failed to delete account: {msg}\n"
                    f"खाता हटाने में विफल: {msg}"
                )
