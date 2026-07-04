import time
from core.common.logger import get_logger


class TransactionHistory:
    def __init__(self):
        self.logger = get_logger("history")
        self.transactions = []

    # -------------------------
    # ADD TX
    # -------------------------
    def add(self, tx_type, status, signature=None, meta=None):
        tx = {
            "type": tx_type,
            "status": status,
            "signature": signature,
            "meta": meta or {},
            "timestamp": time.time()
        }

        self.transactions.append(tx)

        self.logger.info(f"TX recorded: {tx_type} | {status}")

    # -------------------------
    # GET ALL
    # -------------------------
    def get_all(self):
        return self.transactions

    # -------------------------
    # FILTER BY TYPE
    # -------------------------
    def filter(self, tx_type):
        return [tx for tx in self.transactions if tx["type"] == tx_type]

    # -------------------------
    # LAST TX
    # -------------------------
    def last(self):
        return self.transactions[-1] if self.transactions else None