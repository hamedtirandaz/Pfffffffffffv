"""
==============================================================
styles.py

مدیریت استایل برنامه

وظایف:

✔ بارگذاری فایل QSS
✔ تغییر Theme
✔ اعمال Style به برنامه

==============================================================
"""

from pathlib import Path

from core.common.constants import PathConstants


class StyleManager:
    """
    مدیریت استایل برنامه
    """

    def __init__(self):

        # نام Theme فعال
        self.current_theme = "dark"

    # ======================================================
    # مسیر فایل QSS
    # ======================================================

    def get_style_path(self):

        """
        برگرداندن مسیر فایل استایل
        """

        if self.current_theme == "dark":

            return Path(

                "assets/style/dark.qss"

            )

        return Path(

            "assets/style/light.qss"

        )

    # ======================================================
    # خواندن فایل QSS
    # ======================================================

    def load_stylesheet(self):

        """
        خواندن فایل استایل
        """

        style_path = self.get_style_path()

        if not style_path.exists():

            print(

                f"Style file not found : {style_path}"

            )

            return ""

        return style_path.read_text(

            encoding="utf-8"

        )

    # ======================================================
    # تغییر Theme
    # ======================================================

    def set_theme(self, theme):

        """
        تغییر Theme

        dark

        light
        """

        self.current_theme = theme

    # ======================================================
    # گرفتن Theme فعلی
    # ======================================================

    def get_theme(self):

        return self.current_theme


# ==========================================================
# Singleton
# ==========================================================

_style_manager = StyleManager()


# ==========================================================
# توابع کمکی
# ==========================================================

def load_stylesheet():
    """
    استفاده در main.py

    app.setStyleSheet(load_stylesheet())
    """

    return _style_manager.load_stylesheet()


def set_theme(theme):
    """
    تغییر Theme
    """

    _style_manager.set_theme(theme)


def get_theme():
    """
    Theme فعلی
    """

    return _style_manager.get_theme()