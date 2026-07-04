"""
Token Registry

وظیفه:
- نگهداری اطلاعات توکن‌های شناخته‌شده
- تبدیل Mint Address به Symbol
- تعیین نقش (Asset / Trading)
- آماده برای توسعه (Logo, Name, Decimals, Price ...)
"""

from core.common.constants import TokenRole


class TokenRegistry:

    def __init__(self):

        # بعداً از فایل config.json بارگذاری می‌شود
        self._tokens = {}

    # ---------------------------------------------------------
    # Register
    # ---------------------------------------------------------

    def register(
        self,
        symbol: str,
        mint: str,
        role: str = TokenRole.ASSET,
        enabled: bool = True,
    ):

        self._tokens[mint] = {
            "symbol": symbol.upper(),
            "mint": mint,
            "role": role,
            "enabled": enabled,
        }

    # ---------------------------------------------------------
    # Get By Mint
    # ---------------------------------------------------------

    def get(self, mint: str):

        return self._tokens.get(mint)

    # ---------------------------------------------------------
    # Get Symbol
    # ---------------------------------------------------------

    def get_symbol(self, mint: str):

        token = self.get(mint)

        if token:
            return token["symbol"]

        return "UNKNOWN"

    # ---------------------------------------------------------
    # Get Role
    # ---------------------------------------------------------

    def get_role(self, mint: str):

        token = self.get(mint)

        if token:
            return token["role"]

        return TokenRole.ASSET

    # ---------------------------------------------------------
    # Is Enabled
    # ---------------------------------------------------------

    def is_enabled(self, mint: str):

        token = self.get(mint)

        if token is None:
            return False

        return token["enabled"]

    # ---------------------------------------------------------
    # Get All
    # ---------------------------------------------------------

    def get_all(self):

        return list(self._tokens.values())

    # ---------------------------------------------------------
    # Clear
    # ---------------------------------------------------------

    def clear(self):

        self._tokens.clear()

    # ---------------------------------------------------------
    # Count
    # ---------------------------------------------------------

    @property
    def count(self):

        return len(self._tokens)


        # ---------------------------------------------------------
    # Load From Config
    # ---------------------------------------------------------
    def load_from_config(self, config):
        """
        Load tokens from config.json
        """

        self.clear()

        watch_tokens = config.get_watch_tokens()

        for token in watch_tokens:

            self.register(
                symbol=token["symbol"],
                mint=token.get("mint", ""),
                role=token["role"],
                enabled=token.get("enabled", True)
            )