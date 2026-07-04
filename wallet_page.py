# wallet_page.py

from core.wallet import WalletManager


class WalletPage:
    def __init__(
        self,
        wallet_manager: WalletManager,
        config=None,
        parent=None
    ):
        """
        صفحه اتصال کیف پول (GUI Layer)
        """

        self.wallet_manager = wallet_manager
        self.config = config or {}
        self.parent = parent

    # -------------------------
    # اتصال با private key
    # -------------------------
    def connect_with_private_key(self, secret_key_input):
        """
        secret_key_input می‌تواند:
        - Base58 String
        - bytes
        - list[int]
        """

        try:

            wallet_name = self.config.get(
                "wallet_name",
                "Main Wallet"
            )

            self.wallet_manager.connect_from_private_key(
                secret_key_input,
                wallet_name
            )

            public_key = self.wallet_manager.get_public_key()

            # ذخیره آدرس کیف پول در تنظیمات
            self.config["wallet_address"] = public_key

            return {
                "status": "connected",
                "public_key": public_key
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }

    # -------------------------
    # Disconnect
    # -------------------------
    def disconnect(self):

        self.wallet_manager.disconnect()

        return {
            "status": "disconnected"
        }

    # -------------------------
    # وضعیت کیف پول
    # -------------------------
    def get_status(self):

        connected = self.wallet_manager.is_connected()

        return {

            "connected": connected,

            "public_key": (
                self.wallet_manager.get_public_key()
                if connected
                else None
            )

        }