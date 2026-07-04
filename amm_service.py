"""
==============================================================
services/amm_service.py

AMM Service

تمام عملیات مربوط به Pump.fun AMM

در نسخه‌های بعد:

- Create Pool
- Add Liquidity
- Remove Liquidity
- Buy
- Sell

==============================================================
"""

from logger import get_logger

logger = get_logger()
from core.services.base_service import BaseService


class AMMService(BaseService):

    def __init__(
        self,
        rpc,
        wallet_service,
        trading_service,
    ):

        self.rpc = rpc
        self.wallet = wallet_service
        self.trading = trading_service

        logger.info("AMMService initialized")

    async def buy(
        self,
        transaction,
    ):

        logger.info("AMM BUY")

        return await self.trading.send_and_confirm(
            transaction
        )

    async def sell(
        self,
        transaction,
    ):

        logger.info("AMM SELL")

        return await self.trading.send_and_confirm(
            transaction
        )

    async def simulate(
        self,
        transaction,
    ):

        return await self.trading.simulate(
            transaction
        )