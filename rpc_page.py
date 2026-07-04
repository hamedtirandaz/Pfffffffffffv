"""
==============================================================
rpc_page.py

RPC Wizard Page

وظایف:

✔ تنظیم RPC
✔ تست اتصال
✔ ذخیره RPC
✔ اعتبارسنجی آدرس RPC

Author:
Hamed Tirandaz
==============================================================
"""

from __future__ import annotations

from PySide6.QtWidgets import (

    QLabel,

    QPushButton,

    QLineEdit,

)

from gui.pages.base_page import BasePage


class RPCPage(BasePage):

    TITLE = "RPC"

    SUBTITLE = "RPC Configuration"

    DESCRIPTION = """
Configure the Solana RPC endpoint.

A reliable RPC endpoint improves
transaction speed and stability.
"""

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self, config, rpc, parent=None):

        self.config = config

        self.rpc = rpc

        super().__init__(parent)

    # ======================================================
    # UI
    # ======================================================

    def build_body(self):

        self.build_rpc_card()

        self.build_status_card()


    # ======================================================
    # Initialize
    # ======================================================

    def initializePage(self):
        """
        هنگام ورود به صفحه
        """

        super().initializePage()

        self.load_rpc()

    # ======================================================
    # Load
    # ======================================================

    def load_rpc(self):
        """
        بارگذاری RPC ذخیره شده
        """

        rpc_url = self.config.get(

            "rpc_url",

            "https://api.mainnet-beta.solana.com"

        )

        self.rpc_input.setText(rpc_url)

        self.health_lbl.setText("Not Tested")

        self.network_lbl.setText("-")

        self.slot_lbl.setText("-")

    # ======================================================
    # Save
    # ======================================================

    def save_rpc(self):
        """
        ذخیره RPC
        """

        rpc_url = self.rpc_input.text().strip()

        if not rpc_url:

            self.show_error(

                "RPC URL cannot be empty."

            )

            return

        self.config.set(

            "rpc_url",

            rpc_url

        )

        self.config.save()

        self.show_success(

            "RPC saved successfully."

        )

    # ======================================================
    # Test Connection
    # ======================================================

    def test_connection(self):
        """
        تست اتصال RPC
        """

        rpc_url = self.rpc_input.text().strip()

        if not rpc_url:

            self.show_error(

                "Please enter an RPC URL."

            )

            return

        self.show_busy(

            "Testing connection..."

        )

        try:

            #
            # اگر کلاس RPC شما متد connect دارد:
            #
            # self.rpc.connect(rpc_url)
            #

            if hasattr(self.rpc, "connect"):

                self.rpc.connect(rpc_url)

            # اگر این متدها را داشته باشد
            network = "-"

            slot = "-"

            if hasattr(self.rpc, "get_network"):

                network = self.rpc.get_network()

            if hasattr(self.rpc, "get_slot"):

                slot = str(self.rpc.get_slot())

            self.network_lbl.setText(network)

            self.slot_lbl.setText(slot)

            self.health_lbl.setText("Connected")

            self.show_success(

                "Connection successful."

            )

        except Exception as e:

            self.network_lbl.setText("-")

            self.slot_lbl.setText("-")

            self.health_lbl.setText("Failed")

            self.show_error(

                str(e)

            )

        finally:

            self.hide_busy()

    # ======================================================
    # Validation
    # ======================================================

    def validatePage(self):
        """
        بررسی قبل از رفتن به صفحه بعد
        """

        rpc_url = self.rpc_input.text().strip()

        if not rpc_url:

            self.show_error(

                "Please enter an RPC URL."

            )

            return False

        if not (

            rpc_url.startswith("http://")

            or

            rpc_url.startswith("https://")

        ):

            self.show_error(

                "Invalid RPC URL."

            )

            return False

        return True