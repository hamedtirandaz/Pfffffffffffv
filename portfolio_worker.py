import asyncio

from PySide6.QtCore import QThread, Signal


class PortfolioWorker(QThread):

    loaded = Signal(dict)
    error = Signal(str)

    def __init__(self, token_service):

        super().__init__()

        self.token_service = token_service

    def run(self):

        asyncio.run(
            self._run()
        )

    async def _run(self):

        try:

            wallets = await self.token_service.get_all_wallet_assets()

            self.loaded.emit(
                wallets
            )

        except Exception as e:

            self.error.emit(
                str(e)
            )