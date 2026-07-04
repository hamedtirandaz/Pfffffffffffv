"""
==============================================================
welcome_page.py

صفحه خوش‌آمدگویی Wizard

Author:
Hamed Tirandaz
==============================================================
"""

from PySide6.QtWidgets import (
    QLabel,
)

from gui.pages.base_page import BasePage


class WelcomePage(BasePage):
    """
    صفحه خوش‌آمدگویی
    """

    TITLE = "Welcome"

    SUBTITLE = "Pump.fun AMM Manager"

    DESCRIPTION = """
Welcome to <b>Pump.fun AMM Manager</b>.<br><br>

This wizard will guide you through the initial configuration
of the application.

<br><br>

The setup includes:

<ul>
<li>Wallet configuration</li>
<li>RPC configuration</li>
<li>Token settings</li>
<li>AMM settings</li>
</ul>

Click <b>Next</b> to continue.
"""

    # ==================================================
    # UI
    # ==================================================

    def build_body(self):

        info = QLabel(
            """
<b>Before continuing:</b>

<ul>
<li>Have your Solana private key ready.</li>
<li>Use a reliable RPC endpoint.</li>
<li>Keep your private key secure.</li>
</ul>
"""
        )

        info.setWordWrap(True)

        self.add_widget(info)
