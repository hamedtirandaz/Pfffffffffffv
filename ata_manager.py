from core.common.logger import get_logger
from solana.publickey import PublicKey


class ATAManager:
    def __init__(self, wallet, rpc_url):
        self.wallet = wallet
        self.logger = get_logger("ata")

    def get_or_create_ata(self, mint):
        if not self.wallet.connected:
            raise Exception("Wallet not connected")

        self.logger.info(f"Checking ATA for {mint}")

        ata = f"ATA({self.wallet.public_key},{mint})"

        self.logger.info(f"Using ATA: {ata}")

        return {"ata": ata}