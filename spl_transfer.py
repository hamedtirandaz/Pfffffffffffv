from solana.rpc.api import Client
from solana.publickey import PublicKey

from spl.token.instructions import (
    transfer_checked,
    get_associated_token_address
)

from spl.token.constants import TOKEN_PROGRAM_ID
from solana.transaction import Transaction


class SPLTransfer:
    def __init__(self, wallet, rpc_url):
        self.wallet = wallet
        self.client = Client(rpc_url)

    # -------------------------
    # transfer SPL token
    # -------------------------
    def transfer(self, mint, destination, amount, decimals=9):
        if not self.wallet.connected:
            raise RuntimeError("Wallet not connected")

        owner = self.wallet.public_key

        source_ata = get_associated_token_address(
            PublicKey(owner),
            PublicKey(mint)
        )

        dest_ata = get_associated_token_address(
            PublicKey(destination),
            PublicKey(mint)
        )

        instruction = transfer_checked(
            program_id=TOKEN_PROGRAM_ID,
            source=source_ata,
            mint=PublicKey(mint),
            dest=dest_ata,
            owner=owner,
            amount=amount,
            decimals=decimals
        )

        tx = Transaction()
        tx.add(instruction)

        result = self.client.send_transaction(
            tx,
            self.wallet.keypair
        )

        return {
            "status": "sent",
            "signature": str(result),
            "from": str(source_ata),
            "to": str(dest_ata),
            "amount": amount
        }