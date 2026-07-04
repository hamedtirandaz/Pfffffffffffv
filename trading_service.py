"""
==============================================================

core/services/trading_service.py

Trading Service

وظایف:

- ساخت تراکنش
- ارسال تراکنش
- تایید تراکنش
- خرید
- فروش
- انتقال
- Burn
- Stake
- Liquidity

==============================================================
"""

from __future__ import annotations

from typing import Optional

from logger import get_logger

# بعداً هدرهای واقعی را اضافه می‌کنیم
# from solders.keypair import Keypair
# from solders.pubkey import Pubkey
# from history.transaction_history import TransactionHistory


class TradingService(BaseService):

    def __init__(self, wallet_manager):

        self.wallet_manager = wallet_manager

        # از همان RPC Client موجود در WalletManager استفاده می‌کنیم
        self.rpc = wallet_manager.get_client()

        # بعداً کامل می‌شود
        self.history = None

        self.logger = get_logger("trading_service")

    # ---------------------------------------------------------
    # Wallet Helpers
    # ---------------------------------------------------------

    def get_wallet(self):

        """
        کیف پول فعال را برمی‌گرداند.
        """

        return self.wallet_manager.get_wallet()

    def get_keypair(self):

        """
        Keypair کیف پول فعال
        """

        wallet = self.get_wallet()

        if wallet is None:

            raise RuntimeError(
                "No active wallet."
            )

        return wallet.keypair

    def get_public_key(self):

        """
        Public Key کیف پول فعال
        """

        wallet = self.get_wallet()

        if wallet is None:

            raise RuntimeError(
                "No active wallet."
            )

        return wallet.public_key

    def get_public_key_by_name(
        self,
        wallet_name: str
    ):

        return self.wallet_manager.get_public_key_by_name(
            wallet_name
        )

    def get_wallet_by_name(
        self,
        wallet_name: str
    ):

        return self.wallet_manager.get_wallet_by_name(
            wallet_name
        )

    def get_keypair_by_name(
        self,
        wallet_name: str
    ):

        wallet = self.get_wallet_by_name(
            wallet_name
        )

        if wallet is None:

            raise RuntimeError(
                f"Wallet '{wallet_name}' not found."
            )

        return wallet.keypair
    


        # ---------------------------------------------------------
    # Transaction Helpers
    # ---------------------------------------------------------

    async def simulate(
        self,
        transaction
    ):

        """
        شبیه سازی تراکنش قبل از ارسال
        """

        self.logger.info(
            "Simulating transaction..."
        )

        return await self.rpc.simulate_transaction(
            transaction
        )

    async def send(
        self,
        transaction
    ):

        """
        ارسال تراکنش
        """

        self.logger.info(
            "Sending transaction..."
        )

        return await self.rpc.send_transaction(
            transaction
        )

    async def confirm(
        self,
        signature,
        commitment="confirmed"
    ):

        """
        تایید شدن تراکنش
        """

        self.logger.info(

            f"Confirming transaction: {signature}"

        )

        return await self.rpc.confirm_transaction(
            signature,
            commitment=commitment
        )

    async def send_and_confirm(
            
        self,
        transaction
    ):

        """
        ارسال و انتظار برای تایید
        """

        signature = await self.send(
            transaction
        )

        if signature is None:

            raise RuntimeError(
                "Transaction was not sent."
            )

        confirmed = await self.confirm(
            signature
        )

        if not confirmed:

            raise RuntimeError(
                "Transaction confirmation failed."
            )

        self.logger.info(

            f"Transaction confirmed: {signature}"

        )

        return signature
    
    async def simulate_send_and_confirm(
        self,
        transaction
    ):

        """
        ابتدا شبیه سازی
        سپس ارسال
        سپس تایید
        """

        simulation = await self.simulate(
            transaction
        )

        if simulation is None:

            raise RuntimeError(
                "Simulation failed."
            )

        return await self.send_and_confirm(
            transaction
        )
    
    # ---------------------------------------------------------
    # Trading Operations
    # ---------------------------------------------------------

    async def create_token(
        self,
        *args,
        **kwargs
    ):

        """
        ساخت توکن جدید
        """

        self.logger.info(
            "Create Token"
        )

        raise NotImplementedError

    async def buy_token(
        self,
        *args,
        **kwargs
    ):

        """
        خرید توکن
        """

        self.logger.info(
            "Buy Token"
        )

        raise NotImplementedError

    async def sell_token(
        self,
        *args,
        **kwargs
    ):

        """
        فروش توکن
        """

        self.logger.info(
            "Sell Token"
        )

        raise NotImplementedError

    async def add_liquidity(
        self,
        *args,
        **kwargs
    ):

        """
        افزودن نقدینگی
        """

        self.logger.info(
            "Add Liquidity"
        )

        raise NotImplementedError

    async def remove_liquidity(
        self,
        *args,
        **kwargs
    ):

        """
        حذف نقدینگی
        """

        self.logger.info(
            "Remove Liquidity"
        )

        raise NotImplementedError

    async def transfer(
        self,
        destination,
        mint,
        amount
    ):

        """
        انتقال SOL یا SPL Token
        """

        self.logger.info(

            f"Transfer {amount}"

        )

        raise NotImplementedError

    async def burn(
        self,
        mint,
        amount
    ):

        """
        سوزاندن توکن
        """

        self.logger.info(

            f"Burn {amount}"

        )

        raise NotImplementedError

    async def stake(
        self,
        mint,
        amount
    ):

        """
        استیک کردن توکن
        """

        self.logger.info(

            f"Stake {amount}"

        )

        raise NotImplementedError    