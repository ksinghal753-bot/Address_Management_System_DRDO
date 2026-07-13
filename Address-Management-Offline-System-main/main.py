"""
ADRDE, DRDO — Address Management System
Main entry point. Manages the top-level window and screen navigation.

Default Admin Credentials (first run):
  Username: admin
  Password: Admin@1234
"""

import sys
import os
import atexit

# Ensure project root is on Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont

from database.db_manager import db
from ui.splash_screen import SplashScreen
from ui.login_screen import LoginScreen
from ui.admin_dashboard import AdminDashboard
from ui.user_dashboard import UserDashboard
from utils.constants import get_app_stylesheet, APP_NAME_EN, ORG_NAME_EN
from utils.settings_manager import app_settings


class MainWindow(QMainWindow):
    """
    Top-level application window.
    Manages navigation between:
      Splash → Login → Admin/User Dashboard → (back to Splash on logout)
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME_EN} — {ORG_NAME_EN}")
        self.setMinimumSize(1100, 700)
        self.resize(1280, 800)

        # Set window icon (if available)
        icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'drdo_logo_clean.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Central stacked widget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Initialise DB
        try:
            db.connect()
        except Exception as e:
            QMessageBox.critical(
                self, "Database Error / डेटाबेस त्रुटि",
                f"Failed to initialise the database:\n{e}\n\n"
                "Please ensure the application has write permission to its directory."
            )
            sys.exit(1)

        # Daily startup backup (non-blocking, best-effort)
        try:
            from modules.backup_manager import startup_backup
            startup_backup()
        except Exception:
            pass

        self._show_splash()

    # ── Screen builders ────────────────────────────────────────────────────────

    def _show_splash(self):
        self._clear_stack()
        splash = SplashScreen()
        splash.role_selected.connect(self._show_login)
        self.stack.addWidget(splash)
        self.stack.setCurrentWidget(splash)

    def _show_login(self, role: str):
        self._clear_stack()
        login = LoginScreen(role=role)
        login.login_success.connect(self._show_dashboard)
        login.go_back.connect(self._show_splash)
        self.stack.addWidget(login)
        self.stack.setCurrentWidget(login)

    def _show_dashboard(self, role: str):
        self._clear_stack()
        if role == "admin":
            dashboard = AdminDashboard()
            dashboard.logout_requested.connect(self._show_splash)
        else:
            dashboard = UserDashboard()
            dashboard.logout_requested.connect(self._show_splash)
        self.stack.addWidget(dashboard)
        self.stack.setCurrentWidget(dashboard)

    def _clear_stack(self):
        """Remove all widgets from the stack."""
        while self.stack.count() > 0:
            w = self.stack.widget(0)
            self.stack.removeWidget(w)
            w.deleteLater()

    def closeEvent(self, event):
        """Clean shutdown — close DB connection."""
        db.close()
        event.accept()


def main():
    # High-DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME_EN)
    app.setOrganizationName("ADRDE, DRDO")
    app.setApplicationVersion("1.0.0")

    # Apply global stylesheet
    app.setStyle("Fusion")
    app.setStyleSheet(get_app_stylesheet(app_settings.get_theme()))

    # Set default font with Devanagari support
    font = QFont("Segoe UI", 10)
    font.setWeight(QFont.Weight.Medium)  # Make text slightly bolder across the system
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    # ── Single-instance guard ──────────────────────────────────────────────
    try:
        from modules.single_instance import acquire_lock, release_lock
        if not acquire_lock():
            _chk_app = QApplication.instance() or QApplication(sys.argv)
            QMessageBox.warning(
                None, "Already Running / पहले से चल रहा है",
                "Address Management System is already running.\n"
                "कृपया टास्कबार में देखें।"
            )
            sys.exit(0)
        atexit.register(release_lock)
    except Exception:
        pass  # Non-critical — allow startup even if guard fails

    main()
