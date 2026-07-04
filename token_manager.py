from solana.rpc.api import Client
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID
from solana.publickey import PublicKey


class TokenManager:
    def __init__(self, wallet, rpc_url):
        self.wallet = wallet
        self.client = Client(rpc_url)

    def create_token(self):
        if not self.wallet.connected:
            raise RuntimeError("Wallet not connected")

        token = Token.create_mint(
            self.client,
            self.wallet.keypair,
            self.wallet.public_key,
            9,
            TOKEN_PROGRAM_ID
        )

        return {
            "mint": str(token.pubkey)
        }