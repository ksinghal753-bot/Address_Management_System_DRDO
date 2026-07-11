"""
Settings Manager — Handles persistent user preferences.
"""

from PySide6.QtCore import QSettings

class AppSettings:
    """Manages application settings using QSettings."""

    def __init__(self):
        self.settings = QSettings("ADRDE", "AddressManagementSystem")

    def get_theme(self) -> str:
        """Returns the current theme ('light' or 'dark'). Defaults to 'light'."""
        return self.settings.value("theme", "light")

    def set_theme(self, theme: str):
        """Sets the current theme."""
        self.settings.setValue("theme", theme)

    def get_language(self) -> str:
        """Returns the current language ('en', 'hi', or 'bilingual'). Defaults to 'bilingual'."""
        return self.settings.value("language", "bilingual")

    def set_language(self, lang: str):
        """Sets the current language."""
        self.settings.setValue("language", lang)


# Global instance
app_settings = AppSettings()
