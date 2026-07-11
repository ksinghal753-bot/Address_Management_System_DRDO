"""
Admin Dashboard — main navigation hub for admin users.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QFrame, QSizePolicy, QStackedWidget, QMessageBox, QApplication
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont

from modules.address_ops import get_address_stats
from modules.auth import current_session, logout
from ui.shared_widgets import HeaderBar, SectionTitle, show_question, CapacityProgressRing, apply_soft_shadow
from utils.constants import COLORS, LABELS, INACTIVITY_TIMEOUT, get_app_stylesheet


class AdminDashboard(QWidget):
    """
    Admin dashboard with navigation grid and embedded sub-screens.
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
        self._update_stats()

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

        # ── Stacked widget (dashboard ↔ sub-screens) ──────────────────────────
        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_dashboard_page())
        # Hook up stack change to update header back button visibility
        self.stack.currentChanged.connect(lambda idx: self.header.back_btn.setVisible(idx > 0) if hasattr(self.header, 'back_btn') else None)
        root.addWidget(self.stack, stretch=1)

        # ── Status bar ────────────────────────────────────────────────────────
        status = QWidget()
        status.setStyleSheet(f"background: {COLORS['primary_dark']};")
        sl = QHBoxLayout(status)
        sl.setContentsMargins(12, 5, 12, 5)

        self.status_lbl = QLabel(
            f"👔 Admin: {current_session.username}  |  "
            "Role: Administrator / व्यवस्थापक"
        )
        self.status_lbl.setStyleSheet(f"color: {COLORS['accent_light']}; font-size: 11px;")
        sl.addWidget(self.status_lbl)
        sl.addStretch()

        self.record_lbl = QLabel("")
        self.record_lbl.setStyleSheet(f"color: {COLORS['accent_light']}; font-size: 11px;")
        sl.addWidget(self.record_lbl)

        root.addWidget(status)

    def _build_dashboard_page(self) -> QWidget:
        page = QWidget()
        page.setStyleSheet(f"background: {COLORS['surface']};")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)

        # Welcome row with CapacityProgressRing
        hdr_row = QHBoxLayout()
        title_vbox = QVBoxLayout()
        title = SectionTitle(
            f"Welcome, {current_session.username}! / स्वागत है, {current_session.username}!"
        )
        title_vbox.addWidget(title)

        sub_lbl = QLabel(
            "Admin Dashboard / व्यवस्थापक डैशबोर्ड  —  "
            "Select an action / कोई कार्य चुनें"
        )
        sub_lbl.setStyleSheet(f"color: {COLORS['text_secondary']};")
        title_vbox.addWidget(sub_lbl)
        hdr_row.addLayout(title_vbox, stretch=1)

        self.capacity_ring = CapacityProgressRing()
        hdr_row.addWidget(self.capacity_ring)
        layout.addLayout(hdr_row)

        # ── Menu grid ─────────────────────────────────────────────────────────
        grid = QGridLayout()
        grid.setSpacing(14)

        menu_items = [
            ("➕", "Add Address / पता जोड़ें", "Add new address records", self._open_add, COLORS["success"]),
            ("👁️", "Address Database / पता डेटाबेस", "View all address records", self._open_view, COLORS["primary"]),
            ("🏢", LABELS["manage_depts"], "Add / Edit departments", self._open_depts, COLORS["primary_light"]),
            ("👥", LABELS["manage_users"], "Add / Edit user accounts", self._open_users, COLORS["primary_light"]),
        ]

        for i, (icon, label, tooltip, action, color) in enumerate(menu_items):
            btn = self._make_dashboard_btn(icon, label, tooltip, color, action)
            grid.addWidget(btn, i // 3, i % 3)

        layout.addLayout(grid)
        layout.addStretch()
        return page

    def _make_dashboard_btn(self, icon: str, label: str, tooltip: str,
                             color: str, action) -> QPushButton:
        btn = QPushButton(f"{icon}\n{label}")
        btn.setObjectName("dashboardButton")
        btn.setToolTip(tooltip)
        btn.setMinimumSize(200, 90)
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
                padding: 16px;
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

    # ── Navigation ────────────────────────────────────────────────────────────

    def _go_to_dashboard(self):
        while self.stack.count() > 1:
            w = self.stack.widget(self.stack.count() - 1)
            self.stack.removeWidget(w)
            w.deleteLater()
        self.stack.setCurrentIndex(0)
        self._update_stats()

    def _go_to_previous_screen(self):
        if self.stack.count() > 1:
            w = self.stack.currentWidget()
            self.stack.removeWidget(w)
            w.deleteLater()
            self.stack.setCurrentIndex(self.stack.count() - 1)
            self._update_stats()

    def _push_screen(self, widget: QWidget):
        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)

    def _open_add(self):
        from ui.address_form import AddressForm
        form = AddressForm(mode="add")
        form.saved.connect(self._go_to_previous_screen)
        form.cancelled.connect(self._go_to_previous_screen)
        self._push_screen(form)

    def _open_search(self):
        from ui.address_view import AddressView
        view = AddressView(role="admin", mode="search")
        view.go_back.connect(self._go_to_previous_screen)
        view.add_new.connect(self._open_add)
        view.edit_record.connect(self._open_edit)
        self._push_screen(view)

    def _open_edit_list(self):
        from ui.address_view import AddressView
        view = AddressView(role="admin", mode="edit")
        view.go_back.connect(self._go_to_previous_screen)
        view.add_new.connect(self._open_add)
        view.edit_record.connect(self._open_edit)
        self._push_screen(view)

    def _open_delete(self):
        from ui.address_view import AddressView
        view = AddressView(role="admin", mode="delete")
        view.go_back.connect(self._go_to_previous_screen)
        view.add_new.connect(self._open_add)
        view.edit_record.connect(self._open_edit)
        self._push_screen(view)

    def _open_view(self):
        from ui.address_view import AddressView
        view = AddressView(role="admin", mode="view")
        view.go_back.connect(self._go_to_previous_screen)
        view.add_new.connect(self._open_add)
        view.edit_record.connect(self._open_edit)
        self._push_screen(view)

    def _open_edit(self, record: dict):
        from ui.address_form import AddressForm
        form = AddressForm(mode="edit", record=record)
        form.saved.connect(self._go_to_previous_screen)
        form.cancelled.connect(self._go_to_previous_screen)
        self._push_screen(form)

    def _open_depts(self):
        from ui.department_manager import DepartmentManager
        dm = DepartmentManager()
        dm.go_back.connect(self._go_to_previous_screen)
        self._push_screen(dm)

    def _open_users(self):
        from ui.user_manager import UserManager
        um = UserManager()
        um.go_back.connect(self._go_to_previous_screen)
        self._push_screen(um)

    def _do_logout(self):
        if show_question(self, "Logout / लॉगआउट",
                         "Are you sure you want to logout?\nक्या आप लॉगआउट करना चाहते हैं?"):
            self._inactivity_timer.stop()
            logout()
            self.logout_requested.emit()

    def _auto_logout(self):
        from ui.shared_widgets import show_warning
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

    def _update_stats(self):
        stats = get_address_stats()
        self.record_lbl.setText(
            f"📊 Records: {stats['total']} / 500 stored"
        )
        if hasattr(self, 'capacity_ring'):
            self.capacity_ring.set_value(stats['total'])
