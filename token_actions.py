class TokenActions:
    def __init__(self, wallet):
        self.wallet = wallet

    def burn(self, mint, amount):
        return {
            "action": "burn",
            "mint": mint,
            "amount": amount
        }

    def stake(self, mint, amount):
        return {
            "action": "stake",
            "mint": mint,
            "amount": amount
        }