from solana.rpc.api import Client


class RPCService:
    def __init__(self, rpc_url):
        self.client = Client(rpc_url)

    def send_tx(self, tx, signer):
        return self.client.send_transaction(tx, signer)