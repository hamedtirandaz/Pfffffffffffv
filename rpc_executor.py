from solana.rpc.api import Client
from core.common.retry import retry
from core.common.logger import get_logger


class RPCExecutor:
    def __init__(self, rpc_url):
        self.client = Client(rpc_url)
        self.logger = get_logger("rpc")

    @retry(times=3, delay=2)
    def send_and_confirm(self, tx, signer):
        try:
            self.logger.info("Sending transaction...")

            resp = self.client.send_transaction(tx, signer)
            signature = resp.value

            self.logger.info(f"Sent: {signature}")

            self.client.confirm_transaction(signature)

            self.logger.info("Confirmed transaction")

            return {
                "signature": str(signature),
                "status": "confirmed"
            }

        except Exception as e:
            self.logger.exception(f"RPC error: {str(e)}")
            raise