"""
User Dashboard — navigation hub for regular users.
Limited access: View, Search, Print only.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QStackedWidget, QApplication
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont

from modules.auth import current_session, logout
from ui.shared_widgets import HeaderBar, SectionTitle, show_question, show_warning, apply_soft_shadow
from utils.constants import COLORS, LABELS, INACTIVITY_TIMEOUT, get_app_stylesheet


class UserDashboard(QWidget):
    """
    User dashboard — restricted to View/Search/Print operations.
    Emits logout_requested() on logout.
    """
    logout_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._inactivity_timer = QTimer(self)
        self._inactivity_timer.setInterval(INACTIVITY_TIMEOUT * 1000)
        self._inactivity_timer.timeout.connect(self._auto_logout)
        self._inactivity_timer.start()
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        from ui.settings_dialog import SettingsDialog
        self.header = HeaderBar(show_back=True, show_auth_controls=True)
        if hasattr(self.header, 'back_btn'):
            self.header.back_btn.setVisible(False)
        self.header.go_back_requested.connect(self._go_to_previous_screen)
        self.header.logout_requested.connect(self.logout_requested.emit)
        
        def _open_settings():
            dlg = SettingsDialog(self)
            dlg.theme_changed.connect(lambda theme: QApplication.instance().setStyleSheet(get_app_stylesheet(theme)))
            dlg.account_deleted.connect(self.logout_requested.emit)
            dlg.exec()
            
        self.header.settings_requested.connect(_open_settings)
        root.addWidget(self.header)

        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_dashboard_page())
        self.stack.currentChanged.connect(lambda idx: self.header.back_btn.setVisible(idx > 0) if hasattr(self.header, 'back_btn') else None)
        root.addWidget(self.stack, stretch=1)

        # Status bar
        status = QWidget()
        status.setStyleSheet(f"background: {COLORS['primary_dark']};")
        sl = QHBoxLayout(status)
        sl.setContentsMargins(12, 5, 12, 5)
        self.status_lbl = QLabel(
            f"👤 User: {current_session.username}  |  "
            "Role: User / उपयोगकर्ता  |  "
            "Read-Only Access / केवल पढ़ने की अनुमति"
        )
        self.status_lbl.setStyleSheet(f"color: {COLORS['accent_light']}; font-size: 11px;")
        sl.addWidget(self.status_lbl)
        root.addWidget(status)

    def _build_dashboard_page(self) -> QWidget:
        page = QWidget()
        page.setStyleSheet(f"background: {COLORS['surface']};")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignTop)

        title = SectionTitle(
            f"Welcome, {current_session.username}! / स्वागत है!"
        )
        layout.addWidget(title)

        sub = QLabel(
            "User Portal / उपयोगकर्ता पोर्टल — "
            "View, Search, and Print Addresses"
        )
        sub.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(sub)

        # Info banner
        info_banner = QLabel(
            "ℹ️  As a User, you can View, Search, and Print addresses.\n"
            "   Email, FAX, and Contact No. will not appear on printouts.\n"
            "ℹ️  उपयोगकर्ता के रूप में, आप पते देख, खोज और प्रिंट कर सकते हैं।\n"
            "   ईमेल, फैक्स और संपर्क नं. प्रिंट में नहीं दिखेंगे।"
        )
        info_banner.setWordWrap(True)
        info_banner.setStyleSheet(f"""
            background: {COLORS['primary_light']};
            color: white;
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 12px;
            line-height: 1.6;
        """)
        layout.addWidget(info_banner)

        layout.addSpacing(10)

        # ── Menu grid (3 items only) ──────────────────────────────────────────
        grid = QGridLayout()
        grid.setSpacing(20)

        menu_items = [
            ("👁️", "Address Database / पता डेटाबेस", "View all address records", self._open_view, COLORS["primary"]),
            ("🚪", LABELS["logout"], "Logout from the system", self._do_logout, COLORS["error"]),
        ]

        for i, (icon, label, tooltip, action, color) in enumerate(menu_items):
            btn = self._make_btn(icon, label, tooltip, color, action)
            grid.addWidget(btn, 0, i)

        layout.addLayout(grid)
        layout.addStretch()
        return page

    def _make_btn(self, icon: str, label: str, tooltip: str,
                  color: str, action) -> QPushButton:
        btn = QPushButton(f"{icon}\n{label}")
        btn.setToolTip(tooltip)
        btn.setMinimumSize(200, 100)
        btn.setFont(QFont("Segoe UI", 12))
        btn.clicked.connect(action)
        btn.clicked.connect(self._reset_inactivity)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['card_bg']};
                color: {COLORS['primary']};
                border: 1px solid {COLORS['border']};
                border-left: 5px solid {color};
                border-radius: 12px;
                padding: 20px;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
            }}
            QPushButton:hover {{
                background: {COLORS['surface']};
                border-color: {color};
            }}
            QPushButton:pressed {{
                border-bottom: 1px solid {color};
                margin-top: 2px;
            }}
        """)
        apply_soft_shadow(btn, radius=8, alpha=30, y_offset=2)
        return btn

    def _go_to_dashboard(self):
        while self.stack.count() > 1:
            w = self.stack.widget(self.stack.count() - 1)
            self.stack.removeWidget(w)
            w.deleteLater()
        self.stack.setCurrentIndex(0)

    def _go_to_previous_screen(self):
        if self.stack.count() > 1:
            w = self.stack.currentWidget()
            self.stack.removeWidget(w)
            w.deleteLater()
            new_top = self.stack.widget(self.stack.count() - 1)
            self.stack.setCurrentWidget(new_top)
            if hasattr(new_top, 'refresh'):
                new_top.refresh()

    def _push_screen(self, widget: QWidget):
        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)

    def _open_search(self):
        from ui.address_view import AddressView
        view = AddressView(role="user", mode="search")
        view.go_back.connect(self._go_to_previous_screen)
        self._push_screen(view)

    def _open_view(self):
        from ui.address_view import AddressView
        view = AddressView(role="user", mode="view")
        view.go_back.connect(self._go_to_previous_screen)
        self._push_screen(view)

    def _do_logout(self):
        if show_question(self, "Logout / लॉगआउट",
                         "Are you sure you want to logout?\nक्या आप लॉगआउट करना चाहते हैं?"):
            self._inactivity_timer.stop()
            logout()
            self.logout_requested.emit()

    def _auto_logout(self):
        show_warning(self, "Session Expired / सत्र समाप्त",
                     "You have been logged out due to inactivity.\n"
                     "निष्क्रियता के कारण आप लॉगआउट हो गए हैं।")
        self._inactivity_timer.stop()
        logout()
        self.logout_requested.emit()

    def _reset_inactivity(self):
        self._inactivity_timer.start()

    def mousePressEvent(self, event):
        self._reset_inactivity()
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        self._reset_inactivity()
        super().keyPressEvent(event)
