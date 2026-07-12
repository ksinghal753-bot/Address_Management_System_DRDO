"""
Constants and bilingual string definitions for ADRDE Address Management System.
"""

# ─── Application Info ─────────────────────────────────────────────────────────
APP_NAME_EN = "Address Management System"
APP_NAME_HI = "पता प्रबंधन प्रणाली"
ORG_NAME_EN = "ADRDE, DRDO"
ORG_NAME_HI = "एडीआरडीई, डीआरडीओ"
FULL_HEADING_EN = "Aeronautical Development & Research Directorate of Explosives"
FULL_HEADING_HI = "वैमानिकी विकास एवं अनुसंधान निदेशालय"

# Envelope constant prefix
ENVELOPE_PREFIX = "ADRDE/AS-QMS"

# Max address records
MAX_ADDRESSES = 500

# Inactivity timeout (seconds)
INACTIVITY_TIMEOUT = 900  # 15 minutes

# Max login attempts before lockout
MAX_LOGIN_ATTEMPTS = 3

# PARA numbers
PARA_OPTIONS = [f"PARA {i}" for i in range(1, 26)]

# Delivery types
DELIVERY_TYPES = [
    "Ordinary / साधारण",
    "Speed Post / स्पीड पोस्ट",
    "Registered / रजिस्टर्ड",
    "Courier / कूरियर",
    "Hand Delivery / हस्त वितरण",
]

# ─── Colour Palette ────────────────────────────────────────────────────────────
# Government-Enterprise Professional Color Scheme (WCAG AAA Accessible)
LIGHT_COLORS = {
    # Clean Government Style — Light Cream & Rich Maroon
    "primary_dark":    "#5C0D0D",   # Dark Maroon
    "primary":         "#7A1212",   # Government Maroon
    "primary_light":   "#9C1F1F",   # Light Maroon
    
    # Secondary / Accent
    "secondary":       "#7A1212",   # Maroon
    "accent":          "#7A1212",   # Maroon
    "accent_light":    "#A59688",   # Soft Cream-Brown
    "accent_dark":     "#5C0D0D",
    
    # Surfaces & Backgrounds
    "surface":         "#F9F6F0",   # Light Cream Background
    "surface_dark":    "#EAE3DB",   # Warm Light Grey
    "surface_darker":  "#D5C9BC",
    
    # Typography (Black / Dark for maximum visibility)
    "text_primary":    "#000000",   # Black
    "text_secondary":  "#2D221E",   # Dark Brown-Charcoal
    "text_tertiary":   "#5C4E49",   # Medium Brown-Grey
    "text_light":      "#FFFFFF",   # White
    
    # Semantic Colors
    "success":         "#1B5E20",   
    "success_light":   "#2E7D32",   
    "warning":         "#B7791F",   
    "warning_light":   "#D69E2E",   
    "error":           "#C53030",   
    "error_light":     "#E53E3E",   
    "info":            "#1A365D",   
    
    # UI Elements
    "border":          "#E2D8CD",   # Soft Cream-Grey Border
    "header_bg":       "#FFFFFF",   # White Header
    "card_bg":         "#FFFFFF",   # Pure White Card
    "table_header":    "#7A1212",   # Maroon Table Header
    "table_alt":       "#F5EFEA",   # Warm Cream Rows
    "shadow":          "rgba(0,0,0,0.06)",
    "shadow_light":    "rgba(0,0,0,0.04)",
}

DARK_COLORS = LIGHT_COLORS  # Force uniform professional light experience

# Compatibility reference
COLORS = LIGHT_COLORS

# ─── Stylesheet ───────────────────────────────────────────────────────────────
def get_app_stylesheet(theme: str = "light"):
    import sys
    import os
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    check_icon = os.path.join(base_path, 'assets', 'checkbox_checked_dark.png').replace('\\', '/')
    c = LIGHT_COLORS
    return f"""
    /* ── Global ── */
    QWidget {{
        font-family: 'Inter', 'Segoe UI', 'Noto Sans Devanagari', sans-serif;
        font-size: 14px;
        color: {c['text_secondary']};
    }}
    
    QCalendarWidget QWidget {{
        background-color: #FFFFFF;
        color: #1E293B;
    }}
    QCalendarWidget QTableView {{
        background-color: #FFFFFF;
        alternate-background-color: #F8FAFC;
        color: #1E293B;
        selection-background-color: #2563EB;
        selection-color: #FFFFFF;
    }}
    QCalendarWidget QTableView::item {{
        background-color: #FFFFFF;
        color: #1E293B;
    }}
    QCalendarWidget QTableView::item:selected {{
        background-color: #2563EB;
        color: #FFFFFF;
    }}
    QCalendarWidget QWidget#qt_calendar_navigationbar {{
        background-color: #FFFFFF;
        border-bottom: 1px solid #E5E7EB;
    }}
    QCalendarWidget QToolButton {{
        color: #1E293B;
        background-color: transparent;
        font-weight: bold;
    }}
    QCalendarWidget QToolButton:hover {{
        background-color: #EFF6FF;
    }}
    QCalendarWidget QSpinBox {{
        background-color: #FFFFFF;
        color: #1E293B;
    }}
    QDateEdit QCalendarWidget QWidget {{
        background-color: #FFFFFF;
        color: #1E293B;
    }}
    QCalendarWidget QMenu {{
        background-color: #FFFFFF;
        color: #1E293B;
        border: 1px solid #E5E7EB;
    }}
    QCalendarWidget QMenu::item {{
        background-color: transparent;
        padding: 6px 24px 6px 24px;
    }}
    QCalendarWidget QMenu::item:selected {{
        background-color: #EFF6FF;
        color: #2563EB;
    }}
    QMenu {{
        background-color: #FFFFFF;
        color: #1E293B;
        border: 1px solid #E5E7EB;
    }}
    QMenu::item:selected {{
        background-color: #EFF6FF;
        color: #2563EB;
    }}
    
    QMainWindow {{
        background-color: {c['surface']};
    }}

    /* ── Header Bar ── */
    #headerBar {{
        background-color: #FFFFFF;
        border-bottom: 2px solid {c['border']};
        min-height: 85px;
    }}
    #orgLabel {{
        color: {c['primary']};
        font-size: 18px;
        font-weight: bold;
    }}
    #subOrgLabel {{
        color: {c['text_tertiary']};
        font-size: 13px;
    }}
    #hindiLabel {{
        color: {c['primary_light']};
        font-size: 14px;
        font-weight: bold;
    }}

    /* ── Splash Screen ── */
    #splashContainer {{
        background-color: {c['surface']};
    }}
    #splashTitle {{
        color: {c['primary']};
        font-size: 24px;
        font-weight: bold;
    }}
    #splashSubtitle {{
        color: {c['text_tertiary']};
        font-size: 15px;
    }}
    #splashHindi {{
        color: {c['text_secondary']};
        font-size: 17px;
    }}
    #roleCard {{
        background: {c['card_bg']};
        border: 1px solid {c['border']};
        border-radius: 12px;
        padding: 16px;
    }}

    /* ── Buttons ── */
    QPushButton {{
        background: {c['primary']};
        color: {c['text_light']};
        border: 1px solid {c['primary_dark']};
        border-bottom: 3px solid {c['primary_dark']};
        border-radius: 8px;
        padding: 6px 16px;
        font-weight: 600;
        font-size: 13px;
        min-height: 32px;
    }}
    QPushButton:hover {{
        background: {c['primary_light']};
        border-color: {c['primary']};
        border-bottom: 3px solid {c['primary']};
    }}
    QPushButton:pressed {{
        background: {c['primary_dark']};
        border-bottom: 1px solid {c['primary_dark']};
        margin-top: 2px;
    }}
    QPushButton:disabled {{
        background: #E5E7EB;
        color: #9CA3AF;
        border: 1px solid #D1D5DB;
        border-bottom: 1px solid #D1D5DB;
        margin-top: 2px;
    }}
    
    #primaryPrintButton {{
        background-color: #8B0000;
        color: #FFFFFF;
        border: 1px solid #600000;
        border-bottom: 3px solid #600000;
        border-radius: 8px;
        padding: 6px 12px;
        font-family: 'Segoe UI', 'Inter', sans-serif;
        font-size: 13px;
        font-weight: 600;
        min-height: 34px;
    }}
    #primaryPrintButton:hover {{
        background-color: #A30000;
        border-color: #730000;
        border-bottom: 3px solid #730000;
    }}
    #primaryPrintButton:pressed {{
        background-color: #730000;
        border-bottom: 1px solid #600000;
        margin-top: 2px;
    }}
    
    #secondaryButton {{
        background-color: #FFFFFF;
        color: #333333;
        border: 1px solid #CBD5E1;
        border-bottom: 3px solid #CBD5E1;
        border-radius: 8px;
        padding: 6px 12px;
        font-family: 'Segoe UI', 'Inter', sans-serif;
        font-size: 13px;
        font-weight: 600;
        min-height: 34px;
    }}
    #secondaryButton:hover {{
        background-color: #F8FAFC;
        border-color: #94A3B8;
        border-bottom: 3px solid #94A3B8;
    }}
    #secondaryButton:pressed {{
        background-color: #F1F5F9;
        border-bottom: 1px solid #64748B;
        margin-top: 2px;
    }}
    
    #dangerDeleteButton, #dangerButton {{
        background-color: #DC2626;
        color: #FFFFFF;
        border: 1px solid #991B1B;
        border-bottom: 3px solid #991B1B;
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 13px;
        font-weight: 600;
        min-height: 34px;
    }}
    #dangerDeleteButton:hover, #dangerButton:hover {{
        background-color: #EF4444;
        border-color: #B91C1C;
        border-bottom: 3px solid #B91C1C;
    }}
    #dangerDeleteButton:pressed, #dangerButton:pressed {{
        background-color: #B91C1C;
        border-bottom: 1px solid #991B1B;
        margin-top: 2px;
    }}
    
    #successButton {{
        background: {c['success']};
        border: 1px solid #144017;
        border-bottom: 3px solid #144017;
    }}
    #successButton:hover {{
        background: {c['success_light']};
        border-color: {c['success']};
        border-bottom: 3px solid {c['success']};
    }}
    #successButton:pressed {{
        background: #144017;
        border-bottom: 1px solid #144017;
        margin-top: 2px;
    }}

    #roleButton {{
        background: #FFFFFF;
        color: {c['primary']};
        border: 1.5px solid {c['border']};
        border-bottom: 3px solid {c['border']};
        border-radius: 12px;
        padding: 14px;
        font-size: 14px;
        font-weight: bold;
    }}
    #roleButton:hover {{
        background: {c['surface_dark']};
        border-color: {c['primary']};
        border-bottom: 3px solid {c['primary']};
    }}
    #roleButton:pressed {{
        background: {c['surface_darker']};
        border-bottom: 1px solid {c['primary']};
        margin-top: 2px;
    }}
    
    #dashboardButton {{
        background: {c['card_bg']};
        color: {c['primary']};
        border: 1px solid {c['border']};
        border-bottom: 3px solid {c['border']};
        border-radius: 12px;
        padding: 16px;
        font-size: 14px;
        font-weight: bold;
        min-height: 80px;
        min-width: 150px;
    }}
    #dashboardButton:hover {{
        background: {c['primary']};
        color: {c['text_light']};
        border-color: {c['primary_dark']};
        border-bottom: 3px solid {c['primary_dark']};
    }}
    #dashboardButton:pressed {{
        border-bottom: 1px solid {c['primary_dark']};
        margin-top: 2px;
    }}

    QAbstractItemView {{
        background-color: #FFFFFF;
        color: #000000;
        selection-background-color: #E2E8F0;
        selection-color: #000000;
        outline: 0px;
        border-radius: 6px;
    }}
    QAbstractItemView::item:hover {{
        background-color: #F8FAFC;
        color: #000000;
    }}

    /* ── Scrollbars ── */
    QScrollBar:vertical {{
        background: #F1F5F9;
        width: 10px;
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical {{
        background: #CBD5E1;
        min-height: 30px;
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: #94A3B8;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QScrollBar:horizontal {{
        background: #F1F5F9;
        height: 10px;
        border-radius: 5px;
    }}
    QScrollBar::handle:horizontal {{
        background: #CBD5E1;
        border-radius: 5px;
        min-width: 30px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background: #94A3B8;
    }}

    /* ── Input Fields ── */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background: #FFFFFF;
        border: 1px solid #D1D5DB;
        border-bottom: 2px solid #D1D5DB;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 14px;
        color: {c['text_primary']};
        selection-background-color: rgba(122, 18, 18, 0.2);
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border: 2px solid {c['primary_light']};
        background: #FFF9F9;
        padding: 7px 11px; /* Compensate for border width increase */
    }}
    QLineEdit:disabled, QTextEdit:disabled {{
        background: {c['surface_dark']};
        color: {c['text_tertiary']};
        border-bottom: 1px solid #D1D5DB;
    }}
    
    QComboBox {{
        background: #FFFFFF;
        border: 1px solid #D1D5DB;
        border-bottom: 2px solid #D1D5DB;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 14px;
        min-height: 24px;
        color: {c['text_primary']};
    }}
    QComboBox:focus {{
        border: 2px solid {c['primary_light']};
        background: #FFF9F9;
        padding: 7px 11px;
    }}
    QComboBox::drop-down {{
        border: none;
        width: 28px;
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid {c['primary']};
        margin-right: 8px;
    }}
    
    QDateEdit {{
        background: #FFFFFF;
        border: 1px solid #D1D5DB;
        border-bottom: 2px solid #D1D5DB;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 14px;
        min-height: 24px;
        color: {c['text_primary']};
    }}
    QDateEdit:focus {{
        border: 2px solid {c['primary_light']};
        background: #FFF9F9;
        padding: 7px 11px;
    }}
    QDateEdit::drop-down {{
        border: none;
        width: 28px;
    }}
    QDateEdit::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid {c['primary']};
        margin-right: 8px;
    }}

    /* ── Dropdown Menus ── */
    QMenu {{
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 6px 0px;
    }}
    QMenu::item {{
        padding: 8px 24px;
        background: transparent;
        color: #1E293B;
        font-size: 14px;
    }}
    QMenu::item:selected {{
        background-color: #F1F5F9;
        color: #0F172A;
    }}

    /* ── QCalendarWidget (Date Picker Calendar) ── */
    QCalendarWidget {{
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
    }}
    QCalendarWidget QWidget#qt_calendar_navigationbar {{
        background-color: #FFFFFF !important;
        border-bottom: 1px solid #E2E8F0 !important;
        border-top-left-radius: 12px;
        border-top-right-radius: 12px;
        padding: 4px;
    }}
    QCalendarWidget QToolButton {{
        color: #1E293B;
        font-size: 14px;
        font-weight: bold;
        background-color: transparent;
        border: none;
        border-radius: 6px;
        margin: 4px;
        padding: 6px;
    }}
    QCalendarWidget QWidget {{
        background-color: #FFFFFF;
        alternate-background-color: #F8FAFC;
    }}
    QCalendarWidget QAbstractItemView {{
        background-color: #FFFFFF;
        color: #1E293B;
    }}
    QCalendarWidget QToolButton:hover {{
        background-color: #E2E8F0;
    }}
    QCalendarWidget QToolButton:pressed {{
        background-color: #CBD5E1;
    }}
    QCalendarWidget QSpinBox {{
        background-color: #FFFFFF;
        color: #0F172A;
        border: 1px solid #CBD5E1;
        border-radius: 4px;
        font-size: 13px;
        font-weight: bold;
        padding: 4px 6px;
        selection-background-color: #E2E8F0;
        selection-color: #0F172A;
    }}
    QCalendarWidget QTableView {{
        background-color: #FFFFFF;
        color: #1E293B;
        alternate-background-color: #F8FAFC;
        selection-background-color: {c['primary_light']};
        selection-color: #FFFFFF;
        border: none;
        outline: 0;
    }}
    QCalendarWidget QTableView:hover {{
        background-color: #FFF5F5;
    }}
    QCalendarWidget QAbstractItemView:enabled {{
        color: #1E293B;
        background-color: #FFFFFF;
        selection-background-color: {c['primary']};
        selection-color: #FFFFFF;
        border: none;
        outline: 0;
    }}
    QCalendarWidget QAbstractItemView:disabled {{
        color: #94A3B8;
    }}
    QCalendarWidget QHeaderView {{
        background-color: #FFFFFF;
        border: none;
    }}
    QCalendarWidget QHeaderView::section {{
        background-color: #FFFFFF;
        color: #64748B;
        font-weight: bold;
        font-size: 12px;
        border: none;
        padding: 4px;
    }}

    /* ── Labels ── */
    QLabel {{
        color: {c['text_secondary']};
    }}
    #fieldLabel {{
        font-weight: 600;
        color: {c['text_tertiary']};
        font-size: 13px;
        margin-bottom: 2px;
    }}
    #sectionTitle {{
        font-size: 18px;
        font-weight: bold;
        color: {c['primary']};
        border-bottom: 1px solid #E2D8CD;
        padding-bottom: 8px;
        margin-bottom: 12px;
        margin-top: 4px;
    }}
    #envelopePreview {{
        background: #FFFFFF;
        border: 1px solid #E2D8CD;
        border-radius: 12px;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        padding: 16px;
        color: {c['text_primary']};
    }}

    /* ── Table ── */
    QTableWidget {{
        background: #FFFFFF;
        gridline-color: #F1F5F9;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        font-size: 13px;
        selection-background-color: #FEF2F2;
        selection-color: {c['primary']};
        outline: none;
    }}
    QTableWidget::item {{
        padding: 10px 8px;
        border-bottom: 1px solid #F8FAFC;
        color: #1E293B;
    }}
    QTableWidget::item:alternate {{
        background: #FAFAFA;
    }}
    QTableWidget::item:hover {{
        background: #FFF5F5;
    }}
    QHeaderView::section {{
        background: {c['primary']};
        color: white;
        padding: 10px 8px;
        font-weight: bold;
        border: none;
        border-right: 1px solid {c['primary_dark']};
        font-size: 13px;
    }}
    QHeaderView::section:first {{
        border-top-left-radius: 10px;
    }}
    QHeaderView::section:last {{
        border-top-right-radius: 10px;
        border-right: none;
    }}

    /* ── GroupBox ── */
    QGroupBox {{
        font-weight: bold;
        font-size: 14px;
        color: {c['primary']};
        border: 1px solid {c['border']};
        border-radius: 12px;
        margin-top: 14px;
        padding-top: 18px;
        background: #FFFFFF;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 16px;
        padding: 0 8px;
        background: {c['surface']};
        color: {c['primary']};
    }}

    /* ── Menu/StatusBar ── */
    QMenuBar {{
        background: {c['primary']};
        color: white;
        font-weight: 500;
    }}
    QMenuBar::item:selected {{
        background: {c['accent']};
        color: {c['text_light']};
    }}
    QStatusBar {{
        background: {c['primary_dark']};
        color: {c['text_light']};
        font-size: 12px;
    }}

    /* ── Tab Widget ── */
    QTabWidget::pane {{
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        background: #FFFFFF;
    }}
    QTabBar::tab {{
        background: #F8FAFC;
        color: #64748B;
        padding: 10px 24px;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        margin-right: 4px;
        font-weight: 600;
        border: 1px solid transparent;
        border-bottom: none;
    }}
    QTabBar::tab:selected {{
        background: {c['primary']};
        color: white;
        border: 1px solid {c['primary_dark']};
        border-bottom: none;
    }}
    QTabBar::tab:hover:!selected {{
        background: #E2E8F0;
        color: #1E293B;
    }}

    /* ── Dialog ── */
    QDialog {{
        background: {c['surface']};
        border-radius: 12px;
    }}

    /* ── Message Box ── */
    QMessageBox {{
        background: {c['surface']};
        color: {c['text_primary']};
    }}
    QMessageBox QPushButton {{
        min-width: 80px;
    }}

    /* ── Splitter ── */
    QCheckBox::indicator, QTableView::indicator {{
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 2px solid #475569;
        background-color: #F8FAFC;
    }}

    QCheckBox::indicator:unchecked:hover, QTableView::indicator:unchecked:hover {{
        border: 2px solid #1E293B;
        background-color: #F1F5F9;
    }}
    
    QCheckBox::indicator:checked, QTableView::indicator:checked {{
        image: url({check_icon});
        border: 2px solid #1a237e;
        background-color: #F8FAFC;
    }}

    QSplitter::handle {{
        background: #E2E8F0;
        width: 2px;
    }}

    QToolTip {{
        background-color: #F8FAFC;
        color: #1E293B;
        border: 1px solid #94A3B8;
        padding: 6px 10px;
        border-radius: 6px;
        font-family: 'Segoe UI', 'Inter', sans-serif;
        font-size: 13px;
        font-weight: 600;
    }}
    """


# ─── Bilingual Labels ─────────────────────────────────────────────────────────
LABELS = {
    # Auth
    "username":         "Username / उपयोगकर्ता नाम",
    "password":         "Password / पासवर्ड",
    "login":            "Login / लॉगिन",
    "logout":           "Logout / लॉगआउट",
    "forgot_password":  "Forgot Password / पासवर्ड भूल गए",

    # Roles
    "admin":            "Admin / व्यवस्थापक",
    "user":             "User / उपयोगकर्ता",
    "select_role":      "Select Role / भूमिका चुनें",

    # Address fields
    "to":               "To / सेवा में",
    "designation":      "Designation / पदनाम",
    "office_name":      "Department/Office Name / विभाग/कार्यालय का नाम",
    "addr_line1":       "Address Line 1 / पता पंक्ति 1",
    "addr_line2":       "Address Line 2 / पता पंक्ति 2",
    "city_state":       "City, State / शहर, राज्य",
    "pin_code":         "PIN Code / पिन कोड",
    "email":            "Email Address / ईमेल पता",
    "fax":              "FAX No. / फैक्स नं.",
    "contact":          "Contact No. / संपर्क नं.",
    "para_no":          "PARA No. / पैरा नं.",
    "date_entry":       "Date / दिनांक",
    "delivery_type":    "By S/P / डाक प्रकार",
    "department":       "Department / विभाग",
    "designation_hi":   "Designation (Hindi) / पदनाम (हिंदी)",

    # Actions
    "add":              "Add Address / पता जोड़ें",
    "edit":             "Edit Address / पता संपादित करें",
    "update":           "Update Address / पता अपडेट करें",
    "delete":           "Delete Address / पता हटाएं",
    "view":             "View Address / पता देखें",
    "search":           "Search Address / पता खोजें",
    "print":            "Print Address / पता प्रिंट करें",
    "confirm":          "Confirm Changes / परिवर्तन की पुष्टि",
    "return":           "Return to Dashboard / डैशबोर्ड पर वापस जाएं",
    "save":             "Save / सहेजें",
    "clear":            "Clear / साफ करें",
    "cancel":           "Cancel / रद्द करें",
    "yes":              "Yes / हाँ",
    "no":               "No / नहीं",
    "close":            "Close / बंद करें",
    "export":           "Export to Excel / एक्सेल में निर्यात",
    "manage_users":     "Manage Users / उपयोगकर्ता प्रबंधन",
    "manage_depts":     "Manage Departments / विभाग प्रबंधन",

    # Messages
    "confirm_delete":   "Are you sure you want to delete this record?\nक्या आप इस रिकॉर्ड को हटाना चाहते हैं?",
    "record_saved":     "Record saved successfully. / रिकॉर्ड सफलतापूर्वक सहेजा गया।",
    "record_updated":   "Record updated successfully. / रिकॉर्ड सफलतापूर्वक अपडेट किया गया।",
    "record_deleted":   "Record deleted successfully. / रिकॉर्ड सफलतापूर्वक हटाया गया।",
    "limit_reached":    "Storage limit of 500 addresses reached!\nअधिकतम 500 पते संग्रहीत किए जा सकते हैं!",
    "login_failed":     "Invalid username or password.\nअमान्य उपयोगकर्ता नाम या पासवर्ड।",
    "account_locked":   "Account locked after 3 failed attempts.\nContact Admin. / 3 असफल प्रयासों के बाद खाता लॉक हो गया।\nव्यवस्थापक से संपर्क करें।",
    "no_records":       "No records found. / कोई रिकॉर्ड नहीं मिला।",
    "select_record":    "Please select a record first.\nकृपया पहले एक रिकॉर्ड चुनें।",
    "fill_required":    "Please fill all required fields.\nकृपया सभी आवश्यक फ़ील्ड भरें।",
    "print_success":    "PDF generated successfully. / PDF सफलतापूर्वक बनाया गया।",
    "session_expired":  "Session expired. Please login again.\nसत्र समाप्त हो गया। कृपया पुनः लॉगिन करें।",
}

# ─── Pre-seeded Departments ───────────────────────────────────────────────────
DEFAULT_DEPARTMENTS = [
    ("ADRDE", "एडीआरडीई"),
    ("AS-QMS", "एएस-क्यूएमएस"),
    ("DRDL", "डीआरडीएल"),
    ("DEAL", "डील"),
    ("DFRL", "डीएफआरएल"),
    ("DRDO HQ", "डीआरडीओ मुख्यालय"),
    ("CEMILAC", "सेमिलैक"),
    ("ADA", "एडीए"),
    ("HAL", "एचएएल"),
    ("Ministry of Defence", "रक्षा मंत्रालय"),
    ("IAF", "भारतीय वायु सेना"),
    ("Army HQ", "सेना मुख्यालय"),
    ("Naval HQ", "नौसेना मुख्यालय"),
    ("Other", "अन्य"),
]


def tr(key: str, lang: str = None) -> str:
    from utils.settings_manager import app_settings
    if lang is None:
        lang = app_settings.get_language()
    val = LABELS.get(key, key)
    if " / " in val:
        parts = val.split(" / ")
        if lang == "en":
            return parts[0]
        elif lang == "hi":
            return parts[1]
        elif lang == "hi_en":
            return f"{parts[1]} / {parts[0]}"
    return val
