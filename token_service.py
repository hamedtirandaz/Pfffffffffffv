
from core.history.transaction_history import TransactionHistory


from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID

from core.services.base_service import BaseService

from solana.rpc.models import TokenAccountOpts

class TokenService(BaseService):

    def __init__(self, wallet_manager):

        super().__init__(wallet_manager)

        self.history = TransactionHistory()


    # ==========================================================
    # Private
    # ==========================================================
    def _get_wallet_address(
        self,
        wallet_name: str | None = None
    ) -> str:

        if wallet_name is None:
            return self.get_public_key()

        return self.get_public_key_by_name(
            wallet_name
        )


    # ==========================================================
    # Balance
    # ==========================================================     
    async def get_sol_balance(self,    wallet_name: str | None = None) -> float:
        
        """
        Return SOL balance of active wallet.
        """

        try:

            address = self._get_wallet_address( wallet_name)

            if not address:
                return 0.0

            response = await self.rpc.get_balance(
                Pubkey.from_string(address)
            )

            lamports = response.value

            return lamports / 1_000_000_000

        except Exception as e:

            self.logger.exception(
                f"Failed to get SOL balance: {e}"
            )

            return 0.0
    
    async def get_spl_tokens(self, wallet_name: str | None = None) -> list:
        """
        Return all SPL tokens in the active wallet.

        Returns:
            [
                {
                    "mint": "...",
                    "amount": 12.34,
                    "decimals": 6
                },
                ...
            ]
        """

        try:

            address = self._get_wallet_address( wallet_name)


            if not address:
                return []

            response = await self.rpc.get_token_accounts_by_owner_json_parsed(
                Pubkey.from_string(address),
                TokenAccountOpts(
                    program_id=TOKEN_PROGRAM_ID
                )
            )

            tokens = []

            for account in response.value:

                info = account.account.data.parsed["info"]

                token_amount = info["tokenAmount"]

                amount = float(token_amount["uiAmount"] or 0)

                if amount <= 0:
                    continue

                tokens.append(
                    {
                        "mint": info["mint"],
                        "amount": amount,
                        "decimals": token_amount["decimals"]
                    }
                )

            return tokens

        except Exception as e:

            self.logger.exception(
                f"Failed to get SPL tokens: {e}"
            )

            return []    


    # ==========================================================
    # Assets
    # ==========================================================
    async def get_wallet_assets(self) -> list:
        """
        Return assets of active wallet.
        """

        wallet_name = self.wallet_manager.get_wallet_name()

        return await self.get_wallet_assets_by_name(
            wallet_name
        )

    async def get_wallet_assets_by_name(self, wallet_name: str ) -> list:

        cached_assets = self.wallet_manager.get_wallet_assets(
            wallet_name
        )

        if cached_assets:
            return cached_assets

        assets = []

        sol_balance = await self.get_sol_balance(
            wallet_name
        )

        assets.append(
            {
                "symbol": "SOL",
                "amount": sol_balance
            }
        )

        assets.extend(
            await self.get_spl_tokens(wallet_name)
        )

        self.wallet_manager.set_wallet_assets(
            wallet_name,
            assets
        )

        return assets

    async def get_all_wallet_assets(self):

        result = {}

        for wallet_name in self.wallet_manager.get_wallet_names():

            result[wallet_name] = (
                await self.get_wallet_assets_by_name(
                    wallet_name
                )
            )
        return result

    async def refresh_wallet_assets(self,wallet_name: str ) -> list:
        """
        Refresh active wallet assets.
        """
                
        #wallet_name = self.wallet_manager.get_wallet_name()

        self.wallet_manager.clear_wallet_assets(
            wallet_name
        )

        return await self.get_wallet_assets()

    async def refresh_all_wallet_assets(self ) -> dict[str, list]:

        result = {}

        for wallet_name in self.wallet_manager.get_wallet_names():

            result[wallet_name] = (
                await self.refresh_wallet_assets(
                    wallet_name
                )
            )

        return result

    
    # ==========================================================
    # PRC
    # ==========================================================
    async def send(
        self,
        transaction
    ):

        return await self.rpc.send_transaction(
            transaction
        )

    async def simulate(
        self,
        transaction
    ):

        return await self.rpc.simulate_transaction(
            transaction
        )

    async def confirm(
            
            self,
            signature
        ):

        return await self.rpc.confirm_transaction(
            signature
        )

    async def send_and_confirm(
        self,
        transaction
        ):

        signature = await self.send(
            transaction
        )

        ok = await self.confirm(
            signature
        )

        if not bool(ok.value):

            raise RuntimeError(
                "Transaction confirmation failed."
            )

        return signature


    # ==========================================================
    # Token Actions
    # ==========================================================
    async def stake(
            self,
            mint,
            amount
        ):

            self.logger.info(

                f"Stake {amount}"

            )

            return {

                "status": "success"

            }

    async def transfer(
            self,
            mint,
            destination,
            amount
        ):

            self.logger.info(

                f"Transfer {amount}"

            )

            return {

                "status": "success",

                "signature": None

            }   

    async def create_token_full(
            self
        ):

            self.logger.info(
                "Create Token"
            )

            return {

                "status": "success",

                "signature": None

            }
    
