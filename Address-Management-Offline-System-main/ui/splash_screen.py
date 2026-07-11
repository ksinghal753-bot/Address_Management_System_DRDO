"""
Splash / Role Selection Screen — redesigned with an antigravity HUD tech aesthetic.
Displays floating role cards that levitate on hover with deep glowing shadows.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal, QSize, QPropertyAnimation, QEasingCurve, QPoint, Property
from PySide6.QtGui import QFont, QPixmap, QColor

from ui.shared_widgets import LogoLabel, HudBackgroundWidget, HLine
from utils.constants import COLORS


class FloatingRoleCard(QFrame):
    """
    White role card that floats upwards on hover with soft shadow.
    """
    clicked = Signal()

    def __init__(self, icon: str, title: str, hindi: str, desc: str, parent=None):
        super().__init__(parent)
        self.setObjectName("roleCard")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(250, 210)

        # White card style
        self.setStyleSheet("""
            #roleCard {
                background: #FFFFFF;
                border: 1.5px solid #E2D8CD;
                border-radius: 16px;
            }
        """)

        # Soft drop shadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(25)
        self.shadow.setColor(QColor(0, 0, 0, 25))
        self.shadow.setOffset(0, 8)
        self.setGraphicsEffect(self.shadow)

        # Offset animation for float/drift
        self.anim = QPropertyAnimation(self, b"pos_offset")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.OutQuad)
        self._pos_offset = QPoint(0, 0)
        self._original_pos = None

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        icon_lbl = QLabel(icon)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet("font-size: 46px; background: transparent;")
        layout.addWidget(icon_lbl)

        title_lbl = QLabel(f"{title}\n{hindi}")
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setStyleSheet(
            "color: #7A1212; font-size: 16px; font-weight: bold; background: transparent; "
            "line-height: 1.3;"
        )
        layout.addWidget(title_lbl)

        desc_lbl = QLabel(desc)
        desc_lbl.setAlignment(Qt.AlignCenter)
        desc_lbl.setStyleSheet(
            "color: #5C4E49; font-size: 11px; background: transparent;"
        )
        layout.addWidget(desc_lbl)

    @Property(QPoint)
    def pos_offset(self) -> QPoint:
        return getattr(self, '_pos_offset', QPoint(0, 0))

    @pos_offset.setter
    def pos_offset(self, val: QPoint):
        self._pos_offset = val
        if self._original_pos is not None:
            self.move(self._original_pos + val)

    def enterEvent(self, event):
        if self._original_pos is None:
            self._original_pos = self.pos()
        self.anim.stop()
        self.anim.setStartValue(self._pos_offset)
        self.anim.setEndValue(QPoint(0, -12))
        self.anim.start()

        # Highlight border in maroon and deepen shadow on hover
        self.setStyleSheet("""
            #roleCard {
                background: #FFFFFF;
                border: 2px solid #7A1212;
                border-radius: 16px;
            }
        """)
        self.shadow.setBlurRadius(35)
        self.shadow.setColor(QColor(122, 18, 18, 45))
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._pos_offset)
        self.anim.setEndValue(QPoint(0, 0))
        self.anim.start()

        self.setStyleSheet("""
            #roleCard {
                background: #FFFFFF;
                border: 1.5px solid #E2D8CD;
                border-radius: 16px;
            }
        """)
        self.shadow.setBlurRadius(25)
        self.shadow.setColor(QColor(0, 0, 0, 25))
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class SplashScreen(HudBackgroundWidget):
    """
    Role selection screen with clean cream theme.
    """
    role_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("splashContainer")
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 40, 40, 40)
        root.setSpacing(14)
        root.setAlignment(Qt.AlignCenter)

        # ── Logos ─────────────────────────────────────────────────────────────
        logo_row = QHBoxLayout()
        logo_row.setAlignment(Qt.AlignCenter)
        single_logo = LogoLabel(size=QSize(110, 110))
        logo_row.addWidget(single_logo)
        root.addLayout(logo_row)

        # ── Titles ────────────────────────────────────────────────────────────
        org_lbl = QLabel("ADRDE, DRDO")
        org_lbl.setObjectName("splashTitle")
        org_lbl.setAlignment(Qt.AlignCenter)
        f = QFont("Segoe UI", 28, QFont.Bold)
        org_lbl.setFont(f)
        org_lbl.setStyleSheet("color: #7A1212;")
        root.addWidget(org_lbl)

        hindi_lbl = QLabel("एडीआरडीई, डीआरडीओ")
        hindi_lbl.setObjectName("splashHindi")
        hindi_lbl.setAlignment(Qt.AlignCenter)
        hf = QFont("Segoe UI", 18)
        hindi_lbl.setFont(hf)
        hindi_lbl.setStyleSheet("color: #2D221E;")
        root.addWidget(hindi_lbl)

        sub_lbl = QLabel("Address Management System / पता प्रबंधन प्रणाली")
        sub_lbl.setObjectName("splashSubtitle")
        sub_lbl.setAlignment(Qt.AlignCenter)
        sub_lbl.setStyleSheet("color: #5C4E49;")
        root.addWidget(sub_lbl)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("color: #E2D8CD; max-width: 400px;")
        root.addWidget(divider, alignment=Qt.AlignCenter)

        root.addSpacing(15)

        # ── Role selection prompt ─────────────────────────────────────────────
        select_lbl = QLabel("Select Your Role / अपनी भूमिका चुनें")
        select_lbl.setObjectName("splashSubtitle")
        select_lbl.setAlignment(Qt.AlignCenter)
        sf = QFont("Segoe UI", 14)
        select_lbl.setFont(sf)
        select_lbl.setStyleSheet("color: #7A1212;")
        root.addWidget(select_lbl)

        root.addSpacing(10)

        # ── Levitating Role Cards ─────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(45)
        btn_row.setAlignment(Qt.AlignCenter)

        admin_card = FloatingRoleCard(
            icon="👔",
            title="Admin",
            hindi="व्यवस्थापक",
            desc="Full Access / पूर्ण पहुँच",
        )
        admin_card.clicked.connect(lambda: self.role_selected.emit("admin"))

        user_card = FloatingRoleCard(
            icon="👤",
            title="User",
            hindi="उपयोगकर्ता",
            desc="View / Search / Print\nदेखें / खोजें / प्रिंट",
        )
        user_card.clicked.connect(lambda: self.role_selected.emit("user"))

        btn_row.addWidget(admin_card)
        btn_row.addWidget(user_card)
        root.addLayout(btn_row)

        root.addSpacing(25)

        # Version footer
        ver_lbl = QLabel("v2.0 | Offline Levitation HUD | © ADRDE, DRDO")
        ver_lbl.setAlignment(Qt.AlignCenter)
        ver_lbl.setStyleSheet("color: rgba(224, 247, 255, 0.4); font-size: 11px;")
        root.addWidget(ver_lbl)
