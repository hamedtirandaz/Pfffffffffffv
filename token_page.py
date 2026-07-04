"""
==============================================================
token_page.py

Token Wizard Page

وظایف:

✔ Token Name
✔ Symbol
✔ Description
✔ Image
✔ Decimals
✔ Supply

Author:
Hamed Tirandaz
==============================================================
"""

from __future__ import annotations

from PySide6.QtWidgets import (

    QLineEdit,

    QTextEdit,

    QPushButton,

    QLabel,

    QFileDialog,

    QSpinBox,

)

from gui.pages.base_page import BasePage


class TokenPage(BasePage):

    TITLE = "Token"

    SUBTITLE = "Token Information"

    DESCRIPTION = """
Configure your token before deployment.
"""

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self, config, parent=None):

        self.config = config

        super().__init__(parent)

    # ======================================================
    # UI
    # ======================================================

    def build_body(self):

        self.build_token_card()

        self.build_image_card()

    # ======================================================
    # Initialize
    # ======================================================

    def initializePage(self):
        """
        هنگام ورود به صفحه
        """

        super().initializePage()

        self.load_token()

    # ======================================================
    # Load
    # ======================================================

    def load_token(self):
        """
        بارگذاری اطلاعات توکن از Config
        """

        self.name_input.setText(
            self.config.get("token_name", "")
        )

        self.symbol_input.setText(
            self.config.get("token_symbol", "")
        )

        self.decimals_input.setValue(
            self.config.get("token_decimals", 6)
        )

        self.supply_input.setValue(
            self.config.get("token_supply", 1_000_000)
        )

        image = self.config.get(
            "token_image",
            ""
        )

        if image:

            self.image_lbl.setText(image)

    # ======================================================
    # Image
    # ======================================================

    def select_image(self):
        """
        انتخاب تصویر توکن
        """

        filename, _ = QFileDialog.getOpenFileName(

            self,

            "Select Token Image",

            "",

            "Images (*.png *.jpg *.jpeg *.webp)"

        )

        if not filename:
            return

        self.image_lbl.setText(filename)

    # ======================================================
    # Save
    # ======================================================

    def save_token(self):
        """
        ذخیره اطلاعات توکن
        """

        self.config.set(
            "token_name",
            self.name_input.text().strip()
        )

        self.config.set(
            "token_symbol",
            self.symbol_input.text().strip().upper()
        )

        self.config.set(
            "token_decimals",
            self.decimals_input.value()
        )

        self.config.set(
            "token_supply",
            self.supply_input.value()
        )

        self.config.set(
            "token_image",
            self.image_lbl.text()
        )

        self.config.save()

        self.show_success(
            "Token information saved."
        )

    # ======================================================
    # Validation
    # ======================================================

    def validatePage(self):
        """
        بررسی قبل از رفتن به مرحله بعد
        """

        name = self.name_input.text().strip()

        symbol = self.symbol_input.text().strip()

        if not name:

            self.show_error(
                "Please enter a token name."
            )

            return False

        if not symbol:

            self.show_error(
                "Please enter a token symbol."
            )

            return False

        if len(symbol) > 10:

            self.show_error(
                "Token symbol is too long."
            )

            return False

        self.save_token()

        return True

