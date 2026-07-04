from solana.keypair import Keypair
from solana.publickey import PublicKey


class WalletConnector:
    def __init__(self):
        self.keypair = None
        self.public_key = None
        self.connected = False

    def load_private_key(self, secret_key_bytes: bytes):
        self.keypair = Keypair.from_secret_key(secret_key_bytes)
        self.public_key = self.keypair.public_key
        self.connected = True

        return str(self.public_key)