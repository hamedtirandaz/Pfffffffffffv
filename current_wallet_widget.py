from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from PySide6.QtCore import Qt, QTimer
from qasync import asyncSlot



class CurrentWalletWidget(QWidget):

    def __init__(self, wallet_manager, token_service):
        super().__init__()
        
        print(__file__)

        self.wallet_manager = wallet_manager
        self.token_service = token_service

        self.wallet_label = QLabel()
        self.wallet_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.wallet_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        layout = QVBoxLayout()
        layout.addWidget(self.wallet_label)
        self.setLayout(layout)

        #self.timer.timeout.connect(self._refresh_async)

        


    @asyncSlot()
    async def refresh(self):

        if not self.wallet_manager.is_connected():
            self.wallet_label.setText("<b>No wallet connected</b>")
            return

        wallet_name = self.wallet_manager.get_wallet_name()
        pubkey = self.wallet_manager.get_public_key()

        # IMPORTANT: pass wallet context
        try:
            assets = await self.token_service.get_wallet_assets(wallet_name)
        except TypeError:
            # fallback if API هنوز تغییر نکرده
            assets = await self.token_service.get_wallet_assets()

        if not assets:
            assets = []

        text = f"""
<b>🟢 Wallet Connected</b><br><br>

<b>👛 Name:</b> {wallet_name}<br>
<b>🔑 Address:</b> {pubkey}<br><br>

<b>Assets</b><br>
────────────────────────<br>
"""

        for asset in assets:
            symbol = asset.get("symbol", "UNKNOWN")
            amount = asset.get("amount", 0)

            icon = "🪙"
            if symbol == "SOL":
                icon = "💰"
            elif symbol == "USDT":
                icon = "💵"

            text += f"{icon} <b>{symbol}</b> : {amount}<br>"

        text += "<br><b>Status :</b> Active"

        self.wallet_label.setText(text)


