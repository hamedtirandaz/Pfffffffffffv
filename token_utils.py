from spl.token.instructions import get_associated_token_address
from solana.publickey import PublicKey


def get_token_account(owner, mint):
    return get_associated_token_address(
        PublicKey(owner),
        PublicKey(mint)
    )