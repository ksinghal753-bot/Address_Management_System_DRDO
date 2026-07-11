"""
Shared UI widgets: Header bar, bilingual section titles, message helpers.
"""

import os
import sys
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy,
    QMessageBox, QFrame, QPushButton, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QSize, Signal, QVariantAnimation
from PySide6.QtGui import QPixmap, QFont, QPainter, QColor, QPen, QBrush, QPainterPath, QTransform

from utils.constants import COLORS, LABELS


def get_asset_path(filename: str) -> str:
    """Resolve path to an asset file."""
    if getattr(sys, 'frozen', False):
        if hasattr(sys, '_MEIPASS'):
            base_mei = os.path.join(sys._MEIPASS, 'assets')
            if os.path.exists(os.path.join(base_mei, filename)):
                return os.path.join(base_mei, filename)
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.join(os.path.dirname(__file__), '..', 'assets')
    return os.path.join(base, filename) if getattr(sys, 'frozen', False) \
        else os.path.join(os.path.dirname(__file__), '..', 'assets', filename)


def apply_soft_shadow(widget: QWidget, radius: int = 15, alpha: int = 40, x_offset: int = 0, y_offset: int = 4):
    """
    Apply a native, smooth, soft drop shadow to a PySide6 widget.
    This creates the modern elevation effect requested in the UI modernization.
    """
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(radius)
    shadow.setColor(QColor(0, 0, 0, alpha))
    shadow.setOffset(x_offset, y_offset)
    widget.setGraphicsEffect(shadow)



def create_logo_pixmap(text: str, size: QSize, bg_color: str, text_color: str) -> QPixmap:
    """Create a placeholder logo pixmap with text."""
    px = QPixmap(size)
    px.fill(QColor(bg_color))
    painter = QPainter(px)
    painter.setRenderHint(QPainter.Antialiasing)

    # Outer circle
    pen = QPen(QColor(text_color), 2)
    painter.setPen(pen)
    painter.setBrush(QColor(bg_color))
    margin = 4
    painter.drawEllipse(margin, margin, size.width()-2*margin, size.height()-2*margin)

    # Text
    font = QFont("Arial", 8, QFont.Bold)
    painter.setFont(font)
    painter.setPen(QColor(text_color))
    painter.drawText(px.rect(), Qt.AlignCenter, text)
    painter.end()
    return px


class LogoLabel(QLabel):
    """Circular Logo label showing the official uploaded DRDO seal."""

    def __init__(self, logo_filename: str = "drdo_logo_clean.png", fallback_text: str = "",
                 size: QSize = QSize(80, 80), parent=None):
        super().__init__(parent)
        self.setFixedSize(size)
        self.setAlignment(Qt.AlignCenter)
        self.logo_path = get_asset_path(logo_filename)
        self.size_val = size
        self._load_logo()

    def _load_logo(self):
        if os.path.exists(self.logo_path):
            pix = QPixmap(self.logo_path)
            if not pix.isNull():
                scaled = pix.scaled(self.size_val, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.setPixmap(scaled)
                return
        self.setText("DRDO")
        self.setStyleSheet("font-weight: bold; color: #1E3A8A;")


class HudBackgroundWidget(QWidget):
    """Draws a clean professional warm cream background matching the reference."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #F9F6F0;")


class BackIconButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip("Back")
        self._hover_progress = 0.0
        self._timer = QVariantAnimation(self)
        self._timer.setDuration(200)
        self._timer.setStartValue(0.0)
        self._timer.setEndValue(1.0)
        self._timer.valueChanged.connect(self._update_hover)

    def _update_hover(self, val):
        self._hover_progress = val
        self.update()

    def enterEvent(self, event):
        self._timer.setDirection(QVariantAnimation.Forward)
        self._timer.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._timer.setDirection(QVariantAnimation.Backward)
        self._timer.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background color: #FFFFFF -> #DBEAFE
        bg_color = QColor(
            int(255 + (219 - 255) * self._hover_progress),
            int(255 + (234 - 255) * self._hover_progress),
            int(255 + (254 - 255) * self._hover_progress)
        )
        
        painter.setBrush(QBrush(bg_color))
        painter.setPen(QPen(QColor(226, 216, 205, 100), 1))
        painter.drawEllipse(1, 1, 38, 38)

        # Scale factor: 1.0 -> 1.05
        scale = 1.0 + 0.05 * self._hover_progress

        painter.save()
        painter.translate(20, 20)
        painter.scale(scale, scale)
        
        pen = QPen(QColor("#2563EB"), 2.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        
        # Arrow shaft: (8, 0) to (-8, 0)
        painter.drawLine(8, 0, -8, 0)
        # Chevron: (-3, -5) to (-8, 0) to (-3, 5)
        painter.drawLine(-3, -5, -8, 0)
        painter.drawLine(-3, 5, -8, 0)
        
        painter.restore()


class SettingsIconButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip("Settings")
        self._hover_progress = 0.0
        self._timer = QVariantAnimation(self)
        self._timer.setDuration(200)
        self._timer.setStartValue(0.0)
        self._timer.setEndValue(1.0)
        self._timer.valueChanged.connect(self._update_hover)

    def _update_hover(self, val):
        self._hover_progress = val
        self.update()

    def enterEvent(self, event):
        self._timer.setDirection(QVariantAnimation.Forward)
        self._timer.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._timer.setDirection(QVariantAnimation.Backward)
        self._timer.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background color: transparent to #E3F2FD
        bg_alpha = int(240 * self._hover_progress)
        bg_color = QColor(227, 242, 253, bg_alpha)
        
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(1, 1, 38, 38)

        # Icon color: #4B5563 (medium gray) -> #1E3A8A (dark blue)
        icon_r = int(75 + (30 - 75) * self._hover_progress)
        icon_g = int(85 + (58 - 85) * self._hover_progress)
        icon_b = int(99 + (138 - 99) * self._hover_progress)
        icon_color = QColor(icon_r, icon_g, icon_b)

        pen = QPen(icon_color, 2.2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)

        # Draw a gear/cog shape
        painter.drawEllipse(16, 16, 8, 8)
        painter.drawEllipse(18, 18, 4, 4)
        
        for i in range(8):
            angle = i * 45
            painter.save()
            painter.translate(20, 20)
            painter.rotate(angle)
            painter.drawLine(0, -6, 0, -9)
            painter.restore()


class LogoutIconButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip("Logout")
        self._hover_progress = 0.0
        self._timer = QVariantAnimation(self)
        self._timer.setDuration(200)
        self._timer.setStartValue(0.0)
        self._timer.setEndValue(1.0)
        self._timer.valueChanged.connect(self._update_hover)

    def _update_hover(self, val):
        self._hover_progress = val
        self.update()

    def enterEvent(self, event):
        self._timer.setDirection(QVariantAnimation.Forward)
        self._timer.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._timer.setDirection(QVariantAnimation.Backward)
        self._timer.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background color: transparent to #FEE2E2
        bg_alpha = int(255 * self._hover_progress)
        bg_color = QColor(254, 226, 226, bg_alpha)
        
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(1, 1, 38, 38)

        # Icon color: #4B5563 (medium gray) -> #DC2626 (dark red)
        icon_r = int(75 + (220 - 75) * self._hover_progress)
        icon_g = int(85 + (38 - 85) * self._hover_progress)
        icon_b = int(99 + (38 - 99) * self._hover_progress)
        icon_color = QColor(icon_r, icon_g, icon_b)

        pen = QPen(icon_color, 2.2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)

        # Draw door [ facing right
        painter.drawLine(14, 11, 14, 29)
        painter.drawLine(14, 11, 23, 11)
        painter.drawLine(14, 29, 23, 29)

        # Draw arrow exiting door
        painter.drawLine(18, 20, 28, 20)
        painter.drawLine(24, 16, 28, 20)
        painter.drawLine(24, 24, 28, 20)


class HeaderBar(QWidget):
    """
    Persistent header bar shown on every screen.
    Contains: ADRDE logo | Title | Settings/Logout | DRDO logo
    """
    go_back_requested = Signal()
    logout_requested = Signal()
    settings_requested = Signal()

    def __init__(self, show_back=False, show_auth_controls=False, parent=None):
        super().__init__(parent)
        self.setObjectName("headerBar")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(88)
        self.show_back = show_back
        self.show_auth_controls = show_auth_controls
        self._build()

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(14)

        # ── Left Controls ──
        left_layout = QHBoxLayout()
        if self.show_back:
            self.back_btn = BackIconButton()
            self.back_btn.clicked.connect(self.go_back_requested.emit)
            left_layout.addWidget(self.back_btn)
        
        adrde_logo = LogoLabel("drdo_logo_clean.png", "ADRDE", QSize(68, 68))
        left_layout.addWidget(adrde_logo)
        layout.addLayout(left_layout)

        # ── Centre Title ──
        centre = QVBoxLayout()
        centre.setSpacing(2)
        centre.setAlignment(Qt.AlignCenter)

        title_lbl = QLabel("ADRDE, DRDO")
        title_lbl.setObjectName("orgLabel")
        title_lbl.setAlignment(Qt.AlignCenter)
        f = QFont("Segoe UI", 18, QFont.Bold)
        title_lbl.setFont(f)

        hindi_lbl = QLabel("एडीआरडीई, डीआरडीओ")
        hindi_lbl.setObjectName("hindiLabel")
        hindi_lbl.setAlignment(Qt.AlignCenter)
        hf = QFont("Segoe UI", 13)
        hindi_lbl.setFont(hf)

        sub_lbl = QLabel("Address Management System / पता प्रबंधन प्रणाली")
        sub_lbl.setObjectName("subOrgLabel")
        sub_lbl.setAlignment(Qt.AlignCenter)

        centre.addWidget(title_lbl)
        centre.addWidget(hindi_lbl)
        centre.addWidget(sub_lbl)
        layout.addLayout(centre, stretch=1)

        # ── Right Controls ──
        right_layout = QHBoxLayout()
        right_layout.setSpacing(10)
        
        if self.show_auth_controls:
            self.settings_btn = SettingsIconButton()
            self.settings_btn.clicked.connect(self.settings_requested.emit)
            right_layout.addWidget(self.settings_btn)

            self.logout_btn = LogoutIconButton()
            self.logout_btn.clicked.connect(self.logout_requested.emit)
            right_layout.addWidget(self.logout_btn)

        layout.addLayout(right_layout)


class SectionTitle(QLabel):
    """Bold section title label with underline styling."""

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setObjectName("sectionTitle")
        f = QFont("Segoe UI", 14, QFont.Bold)
        self.setFont(f)


class HLine(QFrame):
    """Horizontal separator line."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setStyleSheet(f"color: {COLORS['border']};")


def show_info(parent, title: str, message: str):
    QMessageBox.information(parent, title, message)


def show_error(parent, title: str, message: str):
    QMessageBox.critical(parent, title, message)


def show_warning(parent, title: str, message: str):
    QMessageBox.warning(parent, title, message)


def show_question(parent, title: str, message: str) -> bool:
    reply = QMessageBox.question(
        parent, title, message,
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    return reply == QMessageBox.Yes


from PySide6.QtCore import Property, QRectF
from PySide6.QtCore import QPropertyAnimation

class CapacityProgressRing(QWidget):
    """Animated circular progress ring showing n / 500 Used."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(68, 68)
        self._value = 0
        self._max_value = 500
        self._animation = QPropertyAnimation(self, b"value")
        self._animation.setDuration(800)
        self.setToolTip("Database Capacity / डेटाबेस क्षमता")

    @Property(int)
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, val: int):
        self._value = val
        self.update()

    def set_value(self, val: int):
        self._animation.stop()
        self._animation.setStartValue(self._value)
        self._animation.setEndValue(val)
        self._animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        is_full = self._value >= self._max_value
        if is_full:
            color_ring = QColor("#DC2626")  # Alert Red
            self.setToolTip("Database Full (500/500)!")
        elif self._value >= 450:
            color_ring = QColor("#D97706")  # Warning Orange
            self.setToolTip(f"Warning: Near Limit ({self._value}/500)")
        else:
            color_ring = QColor("#B8860B")  # Theme Gold Accent
            self.setToolTip(f"Database Capacity: {self._value}/500 used")

        rect = QRectF(6, 6, 56, 56)

        # Background ring
        pen_bg = QPen(QColor("#EAE3DB"), 5)
        painter.setPen(pen_bg)
        painter.drawEllipse(rect)

        # Active progress arc
        pen_arc = QPen(color_ring, 5)
        pen_arc.setCapStyle(Qt.RoundCap)
        painter.setPen(pen_arc)

        angle = -360.0 * (self._value / self._max_value)
        painter.drawArc(rect, 90 * 16, int(angle * 16))

        # Text in center
        painter.setPen(QColor("#000000"))
        font = QFont("Segoe UI", 8, QFont.Bold)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self._value}\n/ 500")
        painter.end()
