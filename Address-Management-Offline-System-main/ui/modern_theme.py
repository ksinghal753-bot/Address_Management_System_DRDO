"""
Modern Professional Theme System for ADRDE Address Management System
Creates a government-enterprise level, professional desktop application UI
with modern cards, shadows, animations, and WCAG accessibility compliance.
"""

from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer, QRect
from PySide6.QtGui import QFont, QColor, QIcon, QPixmap, QCursor
from typing import Optional


class ModernStylesheet:
    """Generate comprehensive modern professional stylesheets."""
    
    @staticmethod
    def get_light_stylesheet() -> str:
        """Generate light theme stylesheet (professional government colors)."""
        return """
        /* ══════════════════════════════════════════════════════════════ */
        /* MODERN PROFESSIONAL GOVERNMENT-ENTERPRISE STYLESHEET (LIGHT)   */
        /* ══════════════════════════════════════════════════════════════ */
        
        /* ── Global Styles ── */
        QWidget {
            font-family: 'Segoe UI', 'Inter', 'Poppins', sans-serif;
            font-size: 14px;
            color: #111827;
            background-color: #F8FAFC;
        }
        
        QMainWindow {
            background-color: #F8FAFC;
        }
        
        /* ── Header Bar - Professional Government Style ── */
        #headerBar {
            background-color: #0F172A;
            border-bottom: 4px solid #0EA5A4;
            min-height: 100px;
            padding: 12px 20px;
            shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        #orgLabel {
            color: #FFFFFF;
            font-size: 18px;
            font-weight: bold;
            letter-spacing: 0.5px;
        }
        
        #subOrgLabel {
            color: #14B8A6;
            font-size: 14px;
            font-weight: 600;
        }
        
        #hindiLabel {
            color: #FBBF24;
            font-size: 13px;
            font-weight: 500;
        }
        
        #headerButton {
            background-color: transparent;
            color: #FFFFFF;
            border: 2px solid #0EA5A4;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 600;
            font-size: 13px;
        }
        
        #headerButton:hover {
            background-color: #0EA5A4;
            color: #0F172A;
            border-color: #0EA5A4;
        }
        
        #headerButton:pressed {
            background-color: #0D9488;
        }
        
        /* ── Sidebar Navigation ── */
        #sidebar {
            background-color: #FFFFFF;
            border-right: 2px solid #E2E8F0;
            min-width: 280px;
            max-width: 280px;
            padding: 0px;
            margin: 0px;
        }
        
        #sidebarMenuItem {
            background-color: transparent;
            color: #374151;
            border: none;
            border-left: 4px solid transparent;
            padding: 14px 20px;
            font-size: 14px;
            font-weight: 500;
            text-align: left;
            min-height: 48px;
            margin: 4px 8px;
            border-radius: 8px;
        }
        
        #sidebarMenuItem:hover {
            background-color: #F1F5F9;
            color: #1E40AF;
            border-left-color: #0EA5A4;
        }
        
        #sidebarMenuItem:pressed,
        #sidebarMenuItemActive {
            background-color: #E0F2FE;
            color: #0F172A;
            border-left-color: #0EA5A4;
            font-weight: 600;
            border-radius: 8px;
        }
        
        #sidebarSection {
            color: #6B7280;
            font-size: 12px;
            font-weight: 700;
            padding: 16px 20px 8px 20px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* ── Professional Cards ── */
        #modernCard {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 20px;
            margin: 12px;
            shadow: 0 2px 8px rgba(0,0,0,0.06);
        }
        
        #modernCard:hover {
            shadow: 0 8px 24px rgba(0,0,0,0.12);
            border-color: #CBD5E1;
        }
        
        #dashboardCard {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 24px;
            margin: 12px;
            shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        
        #dashboardCard:hover {
            shadow: 0 12px 32px rgba(0,0,0,0.12);
            border-color: #0EA5A4;
            transform: translateY(-2px);
        }
        
        #statCard {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #FFFFFF, stop:1 #F8FAFC);
            border: 2px solid #E2E8F0;
            border-radius: 16px;
            padding: 24px;
            margin: 8px;
            shadow: 0 4px 16px rgba(0,0,0,0.08);
        }
        
        #statCard:hover {
            border-color: #0EA5A4;
            shadow: 0 12px 32px rgba(14,165,164,0.15);
        }
        
        #statLabel {
            color: #374151;
            font-size: 13px;
            font-weight: 600;
        }
        
        #statValue {
            color: #0F172A;
            font-size: 32px;
            font-weight: bold;
            margin-top: 8px;
        }
        
        #statSubtitle {
            color: #6B7280;
            font-size: 12px;
            margin-top: 6px;
        }
        
        /* ── Buttons - Modern Professional ── */
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2563EB, stop:1 #1E40AF);
            color: #FFFFFF;
            border: none;
            border-radius: 10px;
            padding: 12px 28px;
            font-weight: 600;
            font-size: 14px;
            min-height: 42px;
            spacing: 8px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #3B82F6, stop:1 #2563EB);
            shadow: 0 4px 16px rgba(30,64,175,0.3);
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #1E40AF, stop:1 #0F172A);
        }
        
        QPushButton:disabled {
            background-color: #D1D5DB;
            color: #6B7280;
            border: none;
            shadow: none;
        }
        
        #primaryButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2563EB, stop:1 #1E40AF);
            color: #FFFFFF;
            border: none;
            border-radius: 10px;
            padding: 12px 28px;
            font-weight: 700;
            font-size: 14px;
            min-height: 42px;
        }
        
        #primaryButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #3B82F6, stop:1 #2563EB);
            shadow: 0 6px 20px rgba(30,64,175,0.4);
        }
        
        #secondaryButton {
            background-color: #FFFFFF;
            color: #1E40AF;
            border: 2px solid #1E40AF;
            border-radius: 10px;
            padding: 10px 26px;
            font-weight: 600;
            font-size: 14px;
            min-height: 42px;
        }
        
        #secondaryButton:hover {
            background-color: #F0F9FF;
            border-color: #0EA5A4;
            color: #0EA5A4;
            shadow: 0 4px 12px rgba(14,165,164,0.2);
        }
        
        #dangerButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #EF5350, stop:1 #DC2626);
            color: #FFFFFF;
            border: none;
            border-radius: 10px;
            padding: 12px 28px;
            font-weight: 700;
            font-size: 14px;
            min-height: 42px;
        }
        
        #dangerButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #F87171, stop:1 #EF4444);
            shadow: 0 6px 20px rgba(220,38,38,0.4);
        }
        
        #successButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #10B981, stop:1 #059669);
            color: #FFFFFF;
            border: none;
            border-radius: 10px;
            padding: 12px 28px;
            font-weight: 700;
            font-size: 14px;
            min-height: 42px;
        }
        
        #successButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #34D399, stop:1 #10B981);
            shadow: 0 6px 20px rgba(5,150,105,0.4);
        }
        
        /* ── Input Fields - Modern ── */
        QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox {
            background-color: #FFFFFF;
            border: 2px solid #E2E8F0;
            border-radius: 10px;
            padding: 10px 16px;
            font-size: 14px;
            color: #111827;
            font-weight: 500;
            selection-background-color: #BFDBFE;
            min-height: 42px;
        }
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
            border: 2px solid #1E40AF;
            background-color: #F8FAFC;
            outline: none;
        }
        
        QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {
            border: 2px solid #0EA5A4;
        }
        
        QLineEdit:disabled {
            background-color: #F1F5F9;
            color: #6B7280;
            border: 2px solid #E2E8F0;
        }
        
        /* ── ComboBox - Modern Dropdown ── */
        QComboBox {
            background-color: #FFFFFF;
            border: 2px solid #E2E8F0;
            border-radius: 10px;
            padding: 8px 16px;
            font-size: 14px;
            color: #111827;
            font-weight: 500;
            min-height: 42px;
        }
        
        QComboBox:focus {
            border: 2px solid #1E40AF;
            background-color: #F8FAFC;
        }
        
        QComboBox:hover {
            border: 2px solid #0EA5A4;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 30px;
            background-color: transparent;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 7px solid #1E40AF;
            margin-right: 8px;
        }
        
        QComboBox QAbstractItemView {
            background-color: #FFFFFF;
            border: 2px solid #E2E8F0;
            border-radius: 8px;
            selection-background-color: #1E40AF;
            selection-color: #FFFFFF;
            outline: none;
        }
        
        QComboBox QAbstractItemView::item {
            padding: 8px 12px;
            border-radius: 4px;
        }
        
        QComboBox QAbstractItemView::item:hover {
            background-color: #EFF6FF;
        }
        
        /* ── Date/Time Edit ── */
        QDateEdit, QTimeEdit, QDateTimeEdit {
            background-color: #FFFFFF;
            border: 2px solid #E2E8F0;
            border-radius: 10px;
            padding: 10px 16px;
            font-size: 14px;
            color: #111827;
            font-weight: 500;
            min-height: 42px;
        }
        
        QDateEdit:focus, QTimeEdit:focus, QDateTimeEdit:focus {
            border: 2px solid #1E40AF;
            background-color: #F8FAFC;
        }
        
        /* ── Labels ── */
        QLabel {
            color: #111827;
            font-size: 14px;
        }
        
        #fieldLabel {
            color: #374151;
            font-weight: 600;
            font-size: 13px;
        }
        
        #sectionTitle {
            color: #0F172A;
            font-size: 22px;
            font-weight: bold;
            margin: 16px 0px 8px 0px;
        }
        
        #subsectionTitle {
            color: #1E40AF;
            font-size: 16px;
            font-weight: 700;
            margin: 12px 0px 6px 0px;
        }
        
        /* ── Tables - Professional Data Display ── */
        QTableWidget {
            background-color: #FFFFFF;
            gridline-color: #E2E8F0;
            border: 2px solid #E2E8F0;
            border-radius: 12px;
            font-size: 13px;
            color: #111827;
            font-weight: 500;
            selection-background-color: #BFDBFE;
            selection-color: #0F172A;
        }
        
        QTableWidget::indicator {
            width: 20px;
            height: 20px;
        }
        
        QTableWidget::indicator:unchecked {
            image: url(assets/checkbox_unchecked_light.png);
        }
        
        QTableWidget::indicator:checked {
            image: url(assets/checkbox_checked_light.png);
        }
        
        QTableWidget::item {
            padding: 12px 14px;
            border-bottom: 1px solid #E2E8F0;
            color: #111827;
        }
        
        QTableWidget::item:selected {
            background-color: #BFDBFE;
            color: #0F172A;
        }
        
        QTableWidget::item:alternate {
            background-color: #F8FAFC;
        }
        
        QHeaderView::section {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #1E40AF, stop:1 #0F172A);
            color: #FFFFFF;
            padding: 12px 14px;
            font-weight: 700;
            font-size: 13px;
            border: none;
            border-right: 1px solid #0F172A;
            text-align: left;
        }
        
        QHeaderView::section:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2563EB, stop:1 #1E40AF);
        }
        
        /* ── GroupBox ── */
        QGroupBox {
            color: #1E40AF;
            border: 2px solid #E2E8F0;
            border-radius: 12px;
            padding-top: 16px;
            padding-left: 16px;
            padding-right: 16px;
            padding-bottom: 16px;
            margin-top: 12px;
            font-weight: 600;
            font-size: 13px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 16px;
            padding: 0px 8px;
            background-color: #FFFFFF;
            color: #1E40AF;
        }
        
        /* ── Scroll Bars ── */
        QScrollBar:vertical {
            background-color: #F1F5F9;
            width: 12px;
            border-radius: 6px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #2563EB, stop:1 #1E40AF);
            border-radius: 6px;
            min-height: 40px;
            margin: 2px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #0EA5A4, stop:1 #0D9488);
        }
        
        QScrollBar:horizontal {
            background-color: #F1F5F9;
            height: 12px;
            border-radius: 6px;
            margin: 0px;
        }
        
        QScrollBar::handle:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2563EB, stop:1 #1E40AF);
            border-radius: 6px;
            min-width: 40px;
            margin: 2px;
        }
        
        
        /* ── Dropdown Menus ── */
        QMenu {
            background-color: #FFFFFF;
            color: #111827;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 4px 0px;
        }
        QMenu::item {
            padding: 6px 24px;
            background: transparent;
        }
        QMenu::item:selected {
            background-color: #F0F9FF;
            color: #0369A1;
        }

        /* ── Menu/Status Bar ── */
        QMenuBar {
            background-color: #0F172A;
            color: #FFFFFF;
            border-bottom: 2px solid #0EA5A4;
        }
        
        QMenuBar::item:selected {
            background-color: #1E40AF;
        }
        
        QStatusBar {
            background-color: #0F172A;
            color: #14B8A6;
            font-size: 11px;
            font-weight: 500;
            padding: 6px 12px;
        }
        
        /* ── Tab Widget ── */
        QTabWidget::pane {
            border: 2px solid #E2E8F0;
            border-radius: 12px;
            background-color: #FFFFFF;
        }
        
        QTabBar::tab {
            background-color: #F1F5F9;
            color: #374151;
            border: 2px solid #E2E8F0;
            border-bottom: none;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            padding: 10px 20px;
            font-weight: 600;
            font-size: 13px;
            margin-right: 2px;
        }
        
        QTabBar::tab:selected {
            background-color: #1E40AF;
            color: #FFFFFF;
            border: 2px solid #1E40AF;
            border-bottom: 3px solid #0EA5A4;
        }
        
        QTabBar::tab:hover:!selected {
            background-color: #E0F2FE;
            border-color: #0EA5A4;
        }
        
        /* ── Dialogs ── */
        QDialog {
            background-color: #F8FAFC;
        }
        
        /* ── TreeView/ListWidget ── */
        QTreeWidget, QListWidget {
            background-color: #FFFFFF;
            border: 2px solid #E2E8F0;
            border-radius: 12px;
            outline: none;
            color: #111827;
            font-size: 13px;
            font-weight: 500;
        }
        
        QTreeWidget::item:hover, QListWidget::item:hover {
            background-color: #F0F9FF;
            border-radius: 6px;
        }
        
        QTreeWidget::item:selected, QListWidget::item:selected {
            background-color: #1E40AF;
            color: #FFFFFF;
            border-radius: 6px;
        }
        """
    
    @staticmethod
    def get_dark_stylesheet() -> str:
        """Generate dark theme stylesheet."""
        return """
        /* ══════════════════════════════════════════════════════════════ */
        /* MODERN PROFESSIONAL GOVERNMENT-ENTERPRISE STYLESHEET (DARK)    */
        /* ══════════════════════════════════════════════════════════════ */
        
        /* ── Global Styles ── */
        QWidget {
            font-family: 'Segoe UI', 'Inter', 'Poppins', sans-serif;
            font-size: 14px;
            color: #F8FAFC;
            background-color: #0F172A;
        }
        
        QMainWindow {
            background-color: #0F172A;
        }
        
        /* ── Header Bar ── */
        #headerBar {
            background-color: #020617;
            border-bottom: 4px solid #0EA5A4;
            min-height: 100px;
            padding: 12px 20px;
            shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        
        #orgLabel {
            color: #FFFFFF;
            font-size: 18px;
            font-weight: bold;
            letter-spacing: 0.5px;
        }
        
        #subOrgLabel {
            color: #14B8A6;
            font-size: 14px;
            font-weight: 600;
        }
        
        #hindiLabel {
            color: #FBBF24;
            font-size: 13px;
            font-weight: 500;
        }
        
        #headerButton {
            background-color: transparent;
            color: #FFFFFF;
            border: 2px solid #0EA5A4;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 600;
            font-size: 13px;
        }
        
        #headerButton:hover {
            background-color: #0EA5A4;
            color: #020617;
            border-color: #0EA5A4;
        }
        
        /* ── Sidebar ── */
        #sidebar {
            background-color: #1E293B;
            border-right: 2px solid #334155;
            min-width: 280px;
            max-width: 280px;
        }
        
        #sidebarMenuItem {
            background-color: transparent;
            color: #CBD5E1;
            border: none;
            border-left: 4px solid transparent;
            padding: 14px 20px;
            font-size: 14px;
            font-weight: 500;
            text-align: left;
            min-height: 48px;
            margin: 4px 8px;
            border-radius: 8px;
        }
        
        #sidebarMenuItem:hover {
            background-color: #334155;
            color: #0EA5A4;
            border-left-color: #0EA5A4;
        }
        
        #sidebarMenuItemActive {
            background-color: #1E40AF;
            color: #FFFFFF;
            border-left-color: #0EA5A4;
            font-weight: 600;
        }
        
        /* ── Cards ── */
        #modernCard {
            background-color: #1E293B;
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 20px;
            shadow: 0 2px 8px rgba(0,0,0,0.4);
        }
        
        #modernCard:hover {
            border-color: #0EA5A4;
            shadow: 0 8px 24px rgba(14,165,164,0.2);
        }
        
        #dashboardCard {
            background-color: #1E293B;
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 24px;
            shadow: 0 4px 12px rgba(0,0,0,0.4);
        }
        
        #dashboardCard:hover {
            border-color: #0EA5A4;
            shadow: 0 12px 32px rgba(14,165,164,0.2);
        }
        
        /* ── Buttons ── */
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #3B82F6, stop:1 #1E40AF);
            color: #FFFFFF;
            border: none;
            border-radius: 10px;
            padding: 12px 28px;
            font-weight: 600;
            font-size: 14px;
            min-height: 42px;
        }
        
        QPushButton:hover {
            shadow: 0 6px 20px rgba(59,130,246,0.4);
        }
        
        #primaryButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #3B82F6, stop:1 #1E40AF);
        }
        
        #secondaryButton {
            background-color: transparent;
            color: #3B82F6;
            border: 2px solid #3B82F6;
            border-radius: 10px;
        }
        
        #secondaryButton:hover {
            background-color: #1E40AF;
            color: #FFFFFF;
        }
        
        /* ── Input Fields ── */
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: #334155;
            border: 2px solid #475569;
            border-radius: 10px;
            padding: 10px 16px;
            color: #F8FAFC;
            font-weight: 500;
            min-height: 42px;
        }
        
        QLineEdit:focus {
            border: 2px solid #0EA5A4;
            background-color: #475569;
        }
        
        /* ── Tables ── */
        QTableWidget {
            background-color: #1E293B;
            gridline-color: #334155;
            border: 2px solid #334155;
            border-radius: 12px;
            color: #F8FAFC;
        }
        
        QTableWidget::indicator {
            width: 20px;
            height: 20px;
        }
        
        QTableWidget::indicator:unchecked {
            image: url(assets/checkbox_unchecked_dark.png);
        }
        
        QTableWidget::indicator:checked {
            image: url(assets/checkbox_checked_dark.png);
        }
        
        QTableWidget::item {
            padding: 12px 14px;
            border-bottom: 1px solid #334155;
        }
        
        QHeaderView::section {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #1E40AF, stop:1 #0F172A);
            color: #FFFFFF;
        }
        """


class ModernCard(QFrame):
    """Professional modern card widget with shadows and hover effects."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("modernCard")
        self.setStyleSheet("""
            #modernCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
                padding: 20px;
                shadow: 0 2px 8px rgba(0,0,0,0.06);
            }
        """)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Add subtle hover animation
        self._setup_hover_animation()
    
    def _setup_hover_animation(self):
        """Setup hover animation."""
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)


class ModernDashboardCard(QFrame):
    """Dashboard statistic card with title, value, and subtitle."""
    
    def __init__(self, title: str, value: str, subtitle: str = "", 
                 icon: Optional[QPixmap] = None, parent=None):
        super().__init__(parent)
        self.setObjectName("dashboardCard")
        self.setStyleSheet("""
            #dashboardCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
                shadow: 0 4px 12px rgba(0,0,0,0.08);
            }
        """)
        self.setMinimumHeight(140)
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(8)
        
        # Title
        title_label = QLabel(title)
        title_label.setObjectName("statLabel")
        title_font = QFont("Segoe UI", 13, QFont.SemiBold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #374151; font-weight: 600;")
        layout.addWidget(title_label)
        
        # Value
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        value_font = QFont("Segoe UI", 28, QFont.Bold)
        value_label.setFont(value_font)
        value_label.setStyleSheet("color: #0F172A; margin-top: 8px;")
        layout.addWidget(value_label)
        
        # Subtitle
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setObjectName("statSubtitle")
            subtitle_font = QFont("Segoe UI", 11)
            subtitle_label.setFont(subtitle_font)
            subtitle_label.setStyleSheet("color: #6B7280; margin-top: 6px;")
            layout.addWidget(subtitle_label)
        
        layout.addStretch()


class ModernButton(QPushButton):
    """Modern professional button with modern styling."""
    
    def __init__(self, text: str, button_type: str = "primary", parent=None):
        super().__init__(text, parent)
        self.button_type = button_type
        self._apply_style()
        
        # Set modern font
        font = QFont("Segoe UI", 13, QFont.Bold)
        self.setFont(font)
        self.setMinimumHeight(42)
        self.setMinimumWidth(120)
        self.setCursor(QCursor(Qt.PointingHandCursor))
    
    def _apply_style(self):
        """Apply modern styling based on button type."""
        if self.button_type == "primary":
            self.setObjectName("primaryButton")
        elif self.button_type == "secondary":
            self.setObjectName("secondaryButton")
        elif self.button_type == "danger":
            self.setObjectName("dangerButton")
        elif self.button_type == "success":
            self.setObjectName("successButton")


class ModernSectionTitle(QLabel):
    """Modern section title with professional styling."""
    
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setObjectName("sectionTitle")
        font = QFont("Segoe UI", 22, QFont.Bold)
        self.setFont(font)
        self.setStyleSheet("color: #0F172A; margin: 16px 0px 12px 0px;")
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)


class ModernSubsectionTitle(QLabel):
    """Modern subsection title."""
    
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setObjectName("subsectionTitle")
        font = QFont("Segoe UI", 16, QFont.Bold)
        self.setFont(font)
        self.setStyleSheet("color: #1E40AF; margin: 12px 0px 8px 0px;")


def create_field_label(text: str) -> QLabel:
    """Create a professional field label."""
    label = QLabel(text)
    label.setObjectName("fieldLabel")
    font = QFont("Segoe UI", 13, QFont.SemiBold)
    label.setFont(font)
    label.setStyleSheet("color: #374151; font-weight: 600;")
    return label
