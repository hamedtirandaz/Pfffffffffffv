from __future__ import annotations

from core.common import get_logger


class BaseService:

    def __init__(self, wallet_manager):

        self.wallet_manager = wallet_manager
        self.rpc = wallet_manager.get_client()
        self.logger = get_logger(self.__class__.__name__)

    # -------------------------------------------------

    def get_wallet(self):

        return self.wallet_manager.get_wallet()

    def get_public_key(self):

        return self.wallet_manager.get_public_key()

    def get_keypair(self):

        wallet = self.get_wallet()

        if wallet is None:
            raise RuntimeError(
                "No active wallet."
            )

        return wallet.keypair

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