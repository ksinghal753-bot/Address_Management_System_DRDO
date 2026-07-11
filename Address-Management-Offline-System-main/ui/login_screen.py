"""
Login Screen — Redesigned to match the clean professional government theme.
Features: cream background (#f0ece4), centered logo badge, Sign In / Sign Up tabs,
Employee ID fields, and password visibility eye toggles.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QStackedWidget, QDialog, QFormLayout,
    QDialogButtonBox, QScrollArea
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QFont, QColor

from modules.auth import attempt_login
from modules.department_ops import add_user, reset_password
from ui.shared_widgets import LogoLabel, show_error, show_info, apply_soft_shadow
from utils.constants import LABELS


class LoginScreen(QWidget):
    """
    Bilingual login screen with Sign In and Sign Up tabs,
    styled in government maroon and cream.
    """
    login_success = Signal(str)
    go_back       = Signal()

    def __init__(self, role: str, parent=None):
        super().__init__(parent)
        self.role = role  # Initial role: 'admin' or 'user'
        self.signup_role = role # Default signup role matches selection
        self._build_ui()

    def _build_ui(self):
        # Set central container background to #f0ece4
        self.setObjectName("loginScreen")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            #loginScreen {
                background-color: #f0ece4;
            }
            QLabel {
                font-family: sans-serif;
            }
        """)

        # Main layout for the entire screen
        screen_layout = QVBoxLayout(self)
        screen_layout.setContentsMargins(20, 20, 20, 20)
        screen_layout.setSpacing(12)

        # Center vertically
        screen_layout.addStretch(1)

        # ── 1. Centered Single Circular Logo ──────────────────────────────────
        logo_container = QHBoxLayout()
        logo_container.setAlignment(Qt.AlignCenter)
        self.logo = LogoLabel(size=QSize(110, 110))
        logo_container.addWidget(self.logo)
        screen_layout.addLayout(logo_container)

        # ── 2. Headings & Subtitles ──────────────────────────────────────────
        title_lbl = QLabel("AERIAL DELIVERY RESEARCH & DEVELOPMENT ESTABLISHMENT")
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setStyleSheet("color: #6b1212; font-size: 16px; font-weight: bold; margin-top: 4px; border: none; background: transparent;")
        screen_layout.addWidget(title_lbl)

        hindi_lbl = QLabel("एयरियल डिलीवरी रिसर्च एंड डेवलपमेंट एस्टेब्लिशमेंट")
        hindi_lbl.setAlignment(Qt.AlignCenter)
        hindi_lbl.setStyleSheet("color: #8b1a1a; font-size: 14px; font-weight: bold; border: none; background: transparent;")
        screen_layout.addWidget(hindi_lbl)

        sub_lbl = QLabel("Defence Research & Development Organisation | Ministry of Defence")
        sub_lbl.setAlignment(Qt.AlignCenter)
        sub_lbl.setStyleSheet("color: #7f7f7f; font-size: 11px; border: none; background: transparent;")
        screen_layout.addWidget(sub_lbl)

        # ── 3. Thin Horizontal Divider with Label ────────────────────────────
        div_row = QHBoxLayout()
        div_row.setContentsMargins(0, 8, 0, 8)
        div_row.setSpacing(15)
        
        l_line = QFrame()
        l_line.setFrameShape(QFrame.HLine)
        l_line.setStyleSheet("color: #e0d9d0; min-width: 80px; background: transparent;")
        r_line = QFrame()
        r_line.setFrameShape(QFrame.HLine)
        r_line.setStyleSheet("color: #e0d9d0; min-width: 80px; background: transparent;")

        div_lbl = QLabel("ADDRESS DIRECTORY")
        div_lbl.setStyleSheet("color: #8c827a; font-weight: bold; font-size: 11px; letter-spacing: 1.5px; border: none; background: transparent;")

        div_row.addStretch(1)
        div_row.addWidget(l_line)
        div_row.addWidget(div_lbl)
        div_row.addWidget(r_line)
        div_row.addStretch(1)
        screen_layout.addLayout(div_row)

        # ── 4. Main White Card Container ─────────────────────────────────────
        self.card = QFrame()
        self.card.setObjectName("cardFrame")
        self.card.setFixedWidth(400)
        self.card.setStyleSheet("""
            #cardFrame {
                background-color: #FFFFFF;
                border: 1px solid #e0d9d0;
                border-radius: 18px;
            }
        """)
        apply_soft_shadow(self.card)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(14)

        # Top row of card: Back button (left) + pill badge (right)
        header_row = QHBoxLayout()
        
        self.back_btn = QPushButton("‹ Back")
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #5c4e49;
                font-size: 14px;
                font-weight: bold;
                padding: 0;
            }
            QPushButton:hover {
                color: #7a1212;
            }
        """)
        self.back_btn.clicked.connect(self.go_back.emit)

        self.role_badge = QLabel()
        self.update_role_badge(self.role)

        header_row.addWidget(self.back_btn, alignment=Qt.AlignLeft)
        header_row.addStretch()
        header_row.addWidget(self.role_badge, alignment=Qt.AlignRight)
        card_layout.addLayout(header_row)

        # Tab Selector: Sign In / Sign Up
        tab_container = QFrame()
        tab_container.setObjectName("tabContainer")
        tab_container.setStyleSheet("""
            #tabContainer {
                background-color: #f0ece4;
                border: none;
                border-radius: 12px;
            }
        """)
        tab_layout = QHBoxLayout(tab_container)
        tab_layout.setContentsMargins(4, 4, 4, 4)
        tab_layout.setSpacing(4)

        self.btn_signin_tab = QPushButton("Sign In")
        self.btn_signup_tab = QPushButton("Sign Up")
        self.btn_signin_tab.setCursor(Qt.PointingHandCursor)
        self.btn_signup_tab.setCursor(Qt.PointingHandCursor)

        self.btn_signin_tab.clicked.connect(lambda: self._set_active_tab("signin"))
        self.btn_signup_tab.clicked.connect(lambda: self._set_active_tab("signup"))

        tab_layout.addWidget(self.btn_signin_tab, stretch=1)
        tab_layout.addWidget(self.btn_signup_tab, stretch=1)
        card_layout.addWidget(tab_container)

        self.form_scroll = QScrollArea()
        self.form_scroll.setWidgetResizable(True)
        self.form_scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self.form_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.form_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Stacked pages
        self.form_stack = QStackedWidget()
        self.form_stack.setObjectName("formStack")
        self.form_stack.setStyleSheet("#formStack { background: transparent; border: none; }")
        self.form_stack.addWidget(self._build_signin_page())
        self.form_stack.addWidget(self._build_signup_page())
        
        self.form_scroll.setWidget(self.form_stack)
        card_layout.addWidget(self.form_scroll)

        # Default tab state
        self._set_active_tab("signin")

        # Center card layout row
        card_row = QHBoxLayout()
        card_row.addStretch(1)
        card_row.addWidget(self.card)
        card_row.addStretch(1)
        screen_layout.addLayout(card_row)

        # Push to center
        screen_layout.addStretch(1)

        # ── 5. Footer ────────────────────────────────────────────────────────
        footer_lbl = QLabel("ADRDE Internal Use Only • Ministry of Defence, Government of India")
        footer_lbl.setAlignment(Qt.AlignCenter)
        footer_lbl.setStyleSheet("""
            QLabel {
                color: #8c827a;
                font-size: 9px;
                margin-top: 10px;
                margin-bottom: 10px;
                border: none;
                background: transparent;
            }
        """)
        screen_layout.addWidget(footer_lbl)

    def update_role_badge(self, role: str):
        role_name = "Administrator" if role == "admin" else "User"
        role_icon = "🛡️" if role == "admin" else "👤"
        self.role_badge.setText(f"{role_icon} {role_name}")
        self.role_badge.setStyleSheet("""
            background-color: #fdf5f5;
            border: 1px solid #7a1212;
            border-radius: 10px;
            padding: 4px 10px;
            color: #7a1212;
            font-weight: bold;
            font-size: 11px;
        """)

    def _set_active_tab(self, tab: str):
        active_qss = """
            QPushButton {
                background-color: #7a1212;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 8px;
                font-weight: bold;
                font-size: 13px;
            }
        """
        inactive_qss = """
            QPushButton {
                background-color: transparent;
                color: #8c827a;
                border: none;
                border-radius: 8px;
                padding: 8px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(122, 18, 18, 0.05);
            }
        """
        if tab == "signin":
            self.btn_signin_tab.setStyleSheet(active_qss)
            self.btn_signup_tab.setStyleSheet(inactive_qss)
            self.form_stack.setCurrentIndex(0)
            self.update_role_badge(self.role)
            self.form_stack.setMinimumHeight(240)
        else:
            self.btn_signin_tab.setStyleSheet(inactive_qss)
            self.btn_signup_tab.setStyleSheet(active_qss)
            self.form_stack.setCurrentIndex(1)
            self.update_role_badge(self.signup_role)
            self.form_stack.setMinimumHeight(440)

    # ── Page Builders ────────────────────────────────────────────────────────

    def _build_signin_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(8)

        # Input styling helper
        input_style = """
            QLineEdit {
                background-color: #faf9f7;
                border: 1px solid #e0dbd4;
                border-radius: 8px;
                padding: 8px 12px;
                color: #2d221e;
                font-size: 13px;
                min-height: 38px;
            }
            QLineEdit:focus {
                border: 1.5px solid #7a1212;
                background-color: #fffcfb;
            }
        """

        # Username / Email
        lbl_email = QLabel("Email Address / Username")
        lbl_email.setStyleSheet("font-weight: bold; color: #5c4e49; font-size: 12px; border: none; background: transparent;")
        self.login_user = QLineEdit()
        self.login_user.setPlaceholderText("your@email.com")
        self.login_user.setStyleSheet(input_style)
        layout.addWidget(lbl_email)
        layout.addWidget(self.login_user)

        # Password Label
        lbl_pass = QLabel("Password / पासवर्ड")
        lbl_pass.setStyleSheet("font-weight: bold; color: #5c4e49; font-size: 12px; border: none; background: transparent;")
        layout.addWidget(lbl_pass)

        self.login_pass = QLineEdit()
        self.login_pass.setEchoMode(QLineEdit.Password)
        self.login_pass.setPlaceholderText("••••••••")
        self.login_pass.setStyleSheet(input_style)
        self.login_pass.setTextMargins(0, 0, 36, 0)
        self.login_pass.returnPressed.connect(self._do_login)

        self.signin_toggle_btn = QPushButton("👁️", self.login_pass)
        self.signin_toggle_btn.setFixedSize(30, 30)
        self.signin_toggle_btn.setCursor(Qt.PointingHandCursor)
        self.signin_toggle_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 0;
            }
        """)
        self.signin_toggle_btn.clicked.connect(lambda: self._toggle_password_visibility(self.login_pass, self.signin_toggle_btn))

        pass_btn_layout = QHBoxLayout(self.login_pass)
        pass_btn_layout.setContentsMargins(0, 0, 8, 0)
        pass_btn_layout.setSpacing(0)
        pass_btn_layout.addStretch()
        pass_btn_layout.addWidget(self.signin_toggle_btn)

        layout.addWidget(self.login_pass)

        # Right-aligned Forgot Password
        forgot_layout = QHBoxLayout()
        forgot_layout.setContentsMargins(0, 0, 0, 0)
        forgot_layout.addStretch()
        self.forgot_btn = QPushButton("Forgot password?")
        self.forgot_btn.setCursor(Qt.PointingHandCursor)
        self.forgot_btn.setStyleSheet("""
            QPushButton {
                color: #7a1212;
                font-size: 12px;
                font-weight: bold;
                background: transparent;
                border: none;
                padding: 0;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        self.forgot_btn.clicked.connect(self._forgot_password)
        forgot_layout.addWidget(self.forgot_btn)
        layout.addLayout(forgot_layout)

        # Error log
        self.signin_err = QLabel("")
        self.signin_err.setWordWrap(True)
        self.signin_err.setStyleSheet("color: #6b1212; font-size: 11px; border: none; background: transparent;")
        self.signin_err.hide()
        layout.addWidget(self.signin_err)

        # Sign In Button
        self.btn_signin = QPushButton("Sign In")
        self.btn_signin.setCursor(Qt.PointingHandCursor)
        self.btn_signin.setStyleSheet("""
            QPushButton {
                background-color: #7a1212;
                color: white;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #6b1212;
            }
        """)
        self.btn_signin.clicked.connect(self._do_login)
        layout.addWidget(self.btn_signin)
        
        # Ensure padding at the bottom of form layout
        layout.addSpacing(2)

        return page

    def _build_signup_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(8)

        # Input styling helper
        input_style = """
            QLineEdit {
                background-color: #faf9f7;
                border: 1px solid #e0dbd4;
                border-radius: 8px;
                padding: 8px 12px;
                color: #2d221e;
                font-size: 13px;
                min-height: 38px;
            }
            QLineEdit:focus {
                border: 1.5px solid #7a1212;
                background-color: #fffcfb;
            }
        """

        # 1. Role Selector Side-by-side cards
        role_label = QLabel("Select Role / भूमिका")
        role_label.setStyleSheet("font-weight: bold; color: #5c4e49; font-size: 12px; border: none; background: transparent;")
        layout.addWidget(role_label)

        role_row = QHBoxLayout()
        role_row.setSpacing(10)

        self.card_admin = QFrame()
        self.card_admin.setObjectName("roleAdminCard")
        self.card_admin.setCursor(Qt.PointingHandCursor)
        self.card_admin.setFixedHeight(65)
        admin_l = QVBoxLayout(self.card_admin)
        admin_l.setAlignment(Qt.AlignCenter)
        admin_l.setContentsMargins(4, 4, 4, 4)
        admin_l.setSpacing(2)
        lbl_admin_emoji = QLabel("👔")
        lbl_admin_emoji.setAlignment(Qt.AlignCenter)
        lbl_admin_emoji.setStyleSheet("font-size: 16px; background: transparent; border: none;")
        lbl_admin_text = QLabel("Admin / व्यवस्थापक")
        lbl_admin_text.setAlignment(Qt.AlignCenter)
        lbl_admin_text.setStyleSheet("font-size: 11px; font-weight: bold; background: transparent; border: none;")
        admin_l.addWidget(lbl_admin_emoji)
        admin_l.addWidget(lbl_admin_text)

        self.card_user = QFrame()
        self.card_user.setObjectName("roleUserCard")
        self.card_user.setCursor(Qt.PointingHandCursor)
        self.card_user.setFixedHeight(65)
        user_l = QVBoxLayout(self.card_user)
        user_l.setAlignment(Qt.AlignCenter)
        user_l.setContentsMargins(4, 4, 4, 4)
        user_l.setSpacing(2)
        lbl_user_emoji = QLabel("👤")
        lbl_user_emoji.setAlignment(Qt.AlignCenter)
        lbl_user_emoji.setStyleSheet("font-size: 16px; background: transparent; border: none;")
        lbl_user_text = QLabel("User / उपयोगकर्ता")
        lbl_user_text.setAlignment(Qt.AlignCenter)
        lbl_user_text.setStyleSheet("font-size: 11px; font-weight: bold; background: transparent; border: none;")
        user_l.addWidget(lbl_user_emoji)
        user_l.addWidget(lbl_user_text)

        self.card_admin.mousePressEvent = lambda event: self._select_signup_role("admin")
        self.card_user.mousePressEvent = lambda event: self._select_signup_role("user")

        role_row.addWidget(self.card_admin, stretch=1)
        role_row.addWidget(self.card_user, stretch=1)
        layout.addLayout(role_row)

        # Apply default styling to role selector cards
        self._select_signup_role(self.signup_role)

        # Spacing after role card row
        layout.addSpacing(16)

        # 2. Side-by-side First Name / Last Name
        names_row = QHBoxLayout()
        names_row.setSpacing(10)

        col_first = QVBoxLayout()
        col_first.setSpacing(4)
        lbl_first = QLabel("First Name")
        lbl_first.setStyleSheet("font-weight: bold; color: #5c4e49; font-size: 12px; border: none; background: transparent;")
        self.signup_first = QLineEdit()
        self.signup_first.setPlaceholderText("First Name")
        self.signup_first.setStyleSheet(input_style)
        col_first.addWidget(lbl_first)
        col_first.addWidget(self.signup_first)

        col_last = QVBoxLayout()
        col_last.setSpacing(4)
        lbl_last = QLabel("Last Name")
        lbl_last.setStyleSheet("font-weight: bold; color: #5c4e49; font-size: 12px; border: none; background: transparent;")
        self.signup_last = QLineEdit()
        self.signup_last.setPlaceholderText("Last Name")
        self.signup_last.setStyleSheet(input_style)
        col_last.addWidget(lbl_last)
        col_last.addWidget(self.signup_last)

        names_row.addLayout(col_first, stretch=1)
        names_row.addLayout(col_last, stretch=1)
        layout.addLayout(names_row)

        # 3. Full-width Email
        lbl_user = QLabel("Email Address")
        lbl_user.setStyleSheet("font-weight: bold; color: #5c4e49; font-size: 12px; border: none; background: transparent;")
        self.signup_user = QLineEdit()
        self.signup_user.setPlaceholderText("your@email.com")
        self.signup_user.setStyleSheet(input_style)
        layout.addWidget(lbl_user)
        layout.addWidget(self.signup_user)



        # 5. Password with Toggle
        lbl_pass = QLabel("Password / पासवर्ड")
        lbl_pass.setStyleSheet("font-weight: bold; color: #5c4e49; font-size: 12px; border: none; background: transparent;")
        layout.addWidget(lbl_pass)

        self.signup_pass = QLineEdit()
        self.signup_pass.setEchoMode(QLineEdit.Password)
        self.signup_pass.setPlaceholderText("••••••••")
        self.signup_pass.setStyleSheet(input_style)
        self.signup_pass.setTextMargins(0, 0, 36, 0)

        self.signup_toggle_btn = QPushButton("👁️", self.signup_pass)
        self.signup_toggle_btn.setFixedSize(30, 30)
        self.signup_toggle_btn.setCursor(Qt.PointingHandCursor)
        self.signup_toggle_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 0;
            }
        """)
        self.signup_toggle_btn.clicked.connect(lambda: self._toggle_password_visibility(self.signup_pass, self.signup_toggle_btn))

        signup_pass_btn_layout = QHBoxLayout(self.signup_pass)
        signup_pass_btn_layout.setContentsMargins(0, 0, 8, 0)
        signup_pass_btn_layout.setSpacing(0)
        signup_pass_btn_layout.addStretch()
        signup_pass_btn_layout.addWidget(self.signup_toggle_btn)

        layout.addWidget(self.signup_pass)

        # Sign Up Error
        self.signup_err = QLabel("")
        self.signup_err.setWordWrap(True)
        self.signup_err.setStyleSheet("color: #6b1212; font-size: 11px; border: none; background: transparent;")
        self.signup_err.hide()
        layout.addWidget(self.signup_err)

        # Submit Sign Up
        self.btn_signup = QPushButton("Create Account")
        self.btn_signup.setCursor(Qt.PointingHandCursor)
        self.btn_signup.setStyleSheet("""
            QPushButton {
                background-color: #7a1212;
                color: white;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #6b1212;
            }
        """)
        self.btn_signup.clicked.connect(self._do_signup)
        layout.addWidget(self.btn_signup)

        # Spacing at bottom
        layout.addSpacing(2)

        return page

    # ── Actions ──────────────────────────────────────────────────────────────

    def _select_signup_role(self, role: str):
        self.signup_role = role
        self.update_role_badge(role)

        selected_style = """
            #roleAdminCard, #roleUserCard {
                background-color: #fdf5f5;
                border: 2px solid #7a1212;
                border-radius: 8px;
            }
            QLabel {
                color: #7a1212;
                background: transparent;
                border: none;
            }
        """
        unselected_style = """
            #roleAdminCard, #roleUserCard {
                background-color: #faf9f7;
                border: 1px solid #e0dbd4;
                border-radius: 8px;
            }
            QLabel {
                color: #5c4e49;
                background: transparent;
                border: none;
            }
        """
        if role == "admin":
            self.card_admin.setStyleSheet(selected_style)
            self.card_user.setStyleSheet(unselected_style)
        else:
            self.card_admin.setStyleSheet(unselected_style)
            self.card_user.setStyleSheet(selected_style)

    def _toggle_password_visibility(self, line_edit: QLineEdit, btn: QPushButton):
        if line_edit.echoMode() == QLineEdit.Password:
            line_edit.setEchoMode(QLineEdit.Normal)
            btn.setText("🙈")
        else:
            line_edit.setEchoMode(QLineEdit.Password)
            btn.setText("👁️")

    def _do_login(self):
        username = self.login_user.text().strip()
        password = self.login_pass.text()

        if not username or not password:
            self._show_signin_error("Please enter credentials.\nक्रेडेंशियल दर्ज करें।")
            return

        self.btn_signin.setEnabled(False)
        self.btn_signin.setText("Verifying... / सत्यापित हो रहा है...")

        result = attempt_login(username, password, self.role)

        self.btn_signin.setEnabled(True)
        self.btn_signin.setText("Sign In")

        if result.success:
            self.signin_err.hide()
            self.login_user.clear()
            self.login_pass.clear()
            self.login_success.emit(result.role)
        else:
            self._show_signin_error(result.message)

    def _do_signup(self):
        import time
        first = self.signup_first.text().strip()
        last = self.signup_last.text().strip()
        username = self.signup_user.text().strip()
        password = self.signup_pass.text()

        if not first or not last or not username or not password:
            self._show_signup_error("Please fill all fields.\nकृपया सभी फ़ील्ड भरें।")
            return

        if len(password) < 8:
            self._show_signup_error("Password must be at least 8 characters.\nपासवर्ड कम से कम 8 अंकों का होना चाहिए।")
            return

        self.btn_signup.setEnabled(False)
        self.btn_signup.setText("Registering... / पंजीकरण हो रहा है...")

        ok, msg = add_user(username, password, self.signup_role, employee_id=f"ADRDE-{int(time.time())}", first_name=first, last_name=last)

        self.btn_signup.setEnabled(True)
        self.btn_signup.setText("Create Account")

        if ok:
            show_info(self, "Sign Up Success", f"Registration completed for '{username}'. You can now Sign In.")
            self.signup_first.clear()
            self.signup_last.clear()
            self.signup_user.clear()
            self.signup_pass.clear()
            self._set_active_tab("signin")
        else:
            self._show_signup_error(msg)

    def _show_signin_error(self, message: str):
        self.signin_err.setText(message)
        self.signin_err.show()
        self.login_pass.clear()

    def _show_signup_error(self, message: str):
        self.signup_err.setText(message)
        self.signup_err.show()
        self.signup_pass.clear()

    def _forgot_password(self):
        dialog = ForgotPasswordDialog(self)
        dialog.exec()


class ForgotPasswordDialog(QDialog):
    """Allow admin to reset a user's password."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Reset Password / पासवर्ड रीसेट")
        self.setFixedWidth(380)
        self.setStyleSheet("background-color: #faf9f7;")
        layout = QVBoxLayout(self)
        layout.setSpacing(14)

        info = QLabel(
            "Enter admin credentials to reset a user's password.\n"
            "व्यवस्थापक क्रेडेंशियल से किसी भी उपयोगकर्ता का पासवर्ड रीसेट करें।"
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #5c4e49; font-size: 12px;")
        layout.addWidget(info)

        form = QFormLayout()
        form.setSpacing(10)

        input_style = """
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #e0dbd4;
                border-radius: 6px;
                padding: 6px 10px;
                color: #2d221e;
            }
            QLineEdit:focus {
                border: 1.5px solid #7a1212;
            }
        """

        self.admin_user = QLineEdit()
        self.admin_user.setPlaceholderText("Admin username")
        self.admin_user.setStyleSheet(input_style)
        self.admin_pass = QLineEdit()
        self.admin_pass.setEchoMode(QLineEdit.Password)
        self.admin_pass.setPlaceholderText("Admin password")
        self.admin_pass.setStyleSheet(input_style)
        self.target_user = QLineEdit()
        self.target_user.setPlaceholderText("Username to reset")
        self.target_user.setStyleSheet(input_style)
        self.new_pass = QLineEdit()
        self.new_pass.setEchoMode(QLineEdit.Password)
        self.new_pass.setPlaceholderText("New password")
        self.new_pass.setStyleSheet(input_style)

        form.addRow("Admin User:", self.admin_user)
        form.addRow("Admin Password:", self.admin_pass)
        form.addRow("Target Username:", self.target_user)
        form.addRow("New Password:", self.new_pass)
        layout.addLayout(form)

        self.msg_lbl = QLabel("")
        self.msg_lbl.setWordWrap(True)
        self.msg_lbl.setStyleSheet("color: #6b1212; font-size: 11px;")
        layout.addWidget(self.msg_lbl)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self._do_reset)
        btns.rejected.connect(self.reject)
        # Style DialogButtonBox buttons to match
        btns.setStyleSheet("""
            QPushButton {
                background-color: #7a1212;
                color: white;
                padding: 6px 14px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #6b1212;
            }
        """)
        layout.addWidget(btns)

    def _do_reset(self):
        from modules.auth import attempt_login
        from modules.department_ops import get_all_users, reset_password as rp

        admin_result = attempt_login(
            self.admin_user.text().strip(),
            self.admin_pass.text(),
            "admin"
        )
        if not admin_result.success:
            self.msg_lbl.setText("Admin authentication failed.\nव्यवस्थापक प्रमाणीकरण विफल।")
            return

        target = self.target_user.text().strip()
        new_pw  = self.new_pass.text()

        if len(new_pw) < 8:
            self.msg_lbl.setText("New password must be at least 8 characters.")
            return

        users = get_all_users()
        user = next((u for u in users if u["username"].lower() == target.lower()), None)
        if not user:
            self.msg_lbl.setText(f"User '{target}' not found.")
            return

        ok, msg = rp(user["user_id"], new_pw)
        if ok:
            show_info(self, "Success", f"Password reset for '{target}'.\n'{target}' का पासवर्ड रीसेट हो गया।")
            self.accept()
        else:
            self.msg_lbl.setText(msg)
