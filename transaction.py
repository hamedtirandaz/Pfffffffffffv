"""
==============================================================
core/transaction.py

مدیریت تراکنش‌های سولانا

وظایف:
- ارسال تراکنش
- شبیه‌سازی تراکنش
- تایید تراکنش
- Encode تراکنش برای لاگ

==============================================================
"""

from __future__ import annotations

from solders.transaction import VersionedTransaction

from core.rpc import SolanaRPC
from logger import get_logger

logger = get_logger()


class TransactionManager:
    """
    مدیریت تراکنش‌های سولانا
    """

    def __init__(self, rpc: SolanaRPC):

        self.rpc = rpc

        logger.info("TransactionManager initialized")

    # ======================================================
    # Send
    # ======================================================

    async def send(
        self,
        transaction: VersionedTransaction,
        skip_preflight: bool = False,
    ) -> str:
        """
        ارسال تراکنش
        """

        logger.info("Sending transaction...")

        return await self.rpc.send_transaction(
            transaction,
            skip_preflight=skip_preflight,
        )

    # ======================================================
    # Simulate
    # ======================================================

    async def simulate(
        self,
        transaction: VersionedTransaction,
    ):
        """
        شبیه‌سازی تراکنش
        """

        logger.info("Simulating transaction...")

        return await self.rpc.simulate_transaction(
            transaction
        )

    # ======================================================
    # Confirm
    # ======================================================

    async def confirm(
        self,
        signature: str,
    ) -> bool:
        """
        انتظار برای تایید تراکنش
        """

        logger.info(
            "Confirm transaction: %s",
            signature,
        )

        return await self.rpc.confirm_transaction(
            signature
        )

    # ======================================================
    # Encode
    # ======================================================

    @staticmethod
    def encode(
        transaction: VersionedTransaction,
    ) -> str:
        """
        تبدیل تراکنش به Base64
        """

        return SolanaRPC.encode_transaction(
            transaction
        )

    # ======================================================
    # Send + Confirm
    # ======================================================

    async def send_and_confirm(
        self,
        transaction: VersionedTransaction,
        skip_preflight: bool = False,
    ) -> str:
        """
        ارسال تراکنش و انتظار برای تایید
        """

        signature = await self.send(
            transaction,
            skip_preflight,
        )

        confirmed = await self.confirm(
            signature
        )

        if not confirmed:

            raise RuntimeError(
                "Transaction confirmation failed."
            )

        logger.info(
            "Transaction confirmed: %s",
            signature,
        )

        return signature