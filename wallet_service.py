"""
==============================================================
wallet_service.py

Wallet Service

مسئول:

✔ اعتبارسنجی Private Key
✔ ساخت Keypair
✔ گرفتن Public Key
✔ گرفتن Balance
✔ Generate Wallet

هیچ کد GUI نباید اینجا نوشته شود.

Author:
Hamed Tirandaz
==============================================================
"""

from __future__ import annotations

from solders.keypair import Keypair

from solders.pubkey import Pubkey

from base58 import b58decode

from typing import Optional


class WalletService:

    def __init__(

        self,

        rpc,

        config

    ):

        self.rpc = rpc

        self.config = config

    # ==================================================
    # Private Key
    # ==================================================

    def get_private_key(self) -> str:

        return self.config.get(

            "private_key",

            ""

        )

    def save_private_key(

        self,

        private_key: str

    ):

        self.config.set(

            "private_key",

            private_key

        )

        self.config.save()

    def clear_private_key(self):

        self.config.set(

            "private_key",

            ""

        )

        self.config.save()

    # ==================================================
    # Validation
    # ==================================================

    def validate_private_key(

        self,

        private_key: str

    ) -> bool:

        if not private_key:

            return False

        try:

            b58decode(

                private_key

            )

            return True

        except Exception:

            return False

    # ==================================================
    # Keypair
    # ==================================================

    def get_keypair(
        self,
        private_key: str | None = None
    ) -> Optional[Keypair]:
        """
        ساخت Keypair از Private Key
        """

        if private_key is None:
            private_key = self.get_private_key()

        if not self.validate_private_key(private_key):
            return None

        try:

            secret = b58decode(private_key)

            return Keypair.from_bytes(secret)

        except Exception:

            return None

    # ==================================================
    # Public Key
    # ==================================================

    def get_public_key(
        self,
        private_key: str | None = None
    ) -> Optional[Pubkey]:
        """
        استخراج Public Key
        """

        keypair = self.get_keypair(private_key)

        if keypair is None:
            return None

        return keypair.pubkey()

    # ==================================================
    # Address
    # ==================================================

    def get_address(
        self,
        private_key: str | None = None
    ) -> str:
        """
        آدرس کیف پول
        """

        pubkey = self.get_public_key(private_key)

        if pubkey is None:
            return ""

        return str(pubkey)

    # ==================================================
    # Generate
    # ==================================================

    def generate_wallet(self) -> tuple[str, str]:
        """
        ساخت کیف پول جدید

        Returns
        -------
        tuple
            (private_key, public_key)
        """

        keypair = Keypair()

        private_key = str(keypair)

        public_key = str(keypair.pubkey())

        return private_key, public_key

    # ==================================================
    # Export
    # ==================================================

    def export_private_key(self) -> str:
        """
        خروجی گرفتن از Private Key
        """

        return self.get_private_key()


    # ==================================================
    # Wallet Status
    # ==================================================

    def wallet_exists(self) -> bool:
        """
        آیا کیف پولی ذخیره شده است؟
        """

        return bool(self.get_private_key())

    # ==================================================
    # Import Wallet
    # ==================================================

    def import_wallet(self, private_key: str) -> bool:
        """
        اعتبارسنجی و ذخیره کیف پول
        """

        if not self.validate_private_key(private_key):
            return False

        self.save_private_key(private_key)

        return True

    # ==================================================
    # Remove Wallet
    # ==================================================

    def remove_wallet(self):
        """
        حذف کیف پول ذخیره شده
        """

        self.clear_private_key()

    # ==================================================
    # Address Validation
    # ==================================================

    def validate_address(
        self,
        address: str
    ) -> bool:
        """
        بررسی معتبر بودن آدرس سولانا
        """

        try:

            Pubkey.from_string(address)

            return True

        except Exception:

            return False

    # ==================================================
    # Balance
    # ==================================================

    def get_balance(
        self,
        address: str | None = None
    ) -> float:
        """
        دریافت موجودی SOL

        اگر آدرس داده نشود،
        از کیف پول ذخیره شده استفاده می‌شود.
        """

        if address is None:

            address = self.get_address()

        if not address:

            return 0.0

        try:

            # انتظار می‌رود rpc دارای این متد باشد
            # مقدار برگشتی بر حسب SOL

            return self.rpc.get_balance(address)

        except Exception:

            return 0.0

    # ==================================================
    # Wallet Info
    # ==================================================

    def get_wallet_info(self) -> dict:
        """
        برگرداندن اطلاعات کامل کیف پول
        """

        address = self.get_address()

        return {

            "private_key": self.get_private_key(),

            "address": address,

            "balance": self.get_balance(address),

            "has_wallet": self.wallet_exists()

        }