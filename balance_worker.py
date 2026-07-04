"""
==============================================================
Balance Worker

دریافت موجودی کیف پول

==============================================================
"""

from PySide6.QtCore import QObject
from PySide6.QtCore import QRunnable
from PySide6.QtCore import Signal

import asyncio


class BalanceWorkerSignals(QObject):

    finished = Signal(float)

    error = Signal(str)


class BalanceWorker(QRunnable):

    def __init__(self, wallet_service, keypair):

        super().__init__()

        self.wallet_service = wallet_service

        self.keypair = keypair

        self.signals = BalanceWorkerSignals()

    def run(self):

        try:

            balance = asyncio.run(

                self.wallet_service.get_balance(

                    self.keypair

                )

            )

            self.signals.finished.emit(

                balance

            )

        except Exception as e:

            self.signals.error.emit(

                str(e)

            )