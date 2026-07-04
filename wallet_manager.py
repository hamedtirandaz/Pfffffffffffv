"""
=========================================================
wallet_manager.py

Professional Wallet Manager

Features
--------
- RPC Client Management
- Base58 Wallet Connection
- Multiple Wallet Support
- Active Wallet
- Public Key
- Keypair
- Ready for Pump.fun SDK
=========================================================
"""

from __future__ import annotations
from core.common.constants import WalletKeys

from dataclasses import dataclass
from typing import Optional, Any

import base58

from solders.keypair import Keypair
from solders.pubkey import Pubkey

from solana.rpc.async_api import AsyncClient

from core.common.logger import get_logger


# =========================================================
# Wallet Model
# =========================================================

@dataclass
class Wallet:

    name: str

    keypair: Keypair

    public_key: Pubkey

    connected: bool = True


# =========================================================
# Wallet Manager
# =========================================================

class WalletManager:
    
    # -----------------------------------------------------
    # Constructor
    # -----------------------------------------------------

    def __init__(self, rpc_url: str):

        self.wallets: dict[str, Wallet] = {}
        self.wallet_assets: dict[str, list[Any]] = {}

        self.logger = get_logger("wallet")

        self.rpc_url = rpc_url

        self.client = AsyncClient(rpc_url)

        
        self.active_wallet: Optional[str] = None

        self.logger.info("WalletManager initialized")

    # -----------------------------------------------------
    # RPC
    # -----------------------------------------------------

    def get_client(self) -> AsyncClient:
        return self.client

    def get_rpc_url(self) -> str:
        return self.rpc_url

    def set_rpc_url(self, rpc_url: str):

        self.rpc_url = rpc_url

        self.client = AsyncClient(rpc_url)

        self.logger.info(f"RPC changed -> {rpc_url}")

    # -----------------------------------------------------
    # Connect Base58 Wallet
    # -----------------------------------------------------
    def connect_from_private_key(
        self,
        private_key: str,
        wallet_name: str = "Main Wallet"
    ) -> Wallet:

        if not private_key:

            raise ValueError("Private key is empty")

        try:

            secret = base58.b58decode(private_key)
            if len(secret) != 64:
                raise ValueError(
                    "Private key must decode to exactly 64 bytes."
                )
            keypair = Keypair.from_bytes(secret)

            wallet = Wallet(

                name=wallet_name,

                keypair=keypair,

                public_key=keypair.pubkey(),

                connected=True

            )
            
            self.wallets[wallet_name] = wallet

            self.active_wallet = wallet_name

            self.logger.info(

                f"Wallet connected: {wallet.public_key}"

            )

            return wallet

        except Exception as e:

            self.logger.exception(e)

            raise

    # -----------------------------------------------------
    # Connect From Config
    # -----------------------------------------------------

    def connect_from_config(self, config):

        wallet = config.get_active_wallet()

        private_key = wallet[WalletKeys.PRIVATE_KEY]

        wallet_name = wallet[WalletKeys.NAME]

        if not private_key:

            self.logger.warning(

                "No private key found inside config"

            )

            return False

        self.connect_from_private_key(

            private_key,

            wallet_name

        )

        return True


    # -----------------------------------------------------
    # Load All Wallets From Config
    # -----------------------------------------------------

    def load_wallets_from_config(self, config) -> bool:
        """
        Load all enabled wallets from config and
        activate the selected wallet.
        """

        try:

            self.clear()

            wallets = config.get_enabled_wallets()

            if not wallets:
                self.logger.warning(
                    "No enabled wallets found."
                )
                return False

            for wallet in wallets:

                private_key = wallet[WalletKeys.PRIVATE_KEY]

                if not private_key:
                    continue

                self.connect_from_private_key(
                    private_key,
                    wallet[WalletKeys.NAME]
                )

            active_wallet = config.get_active_wallet()

            print("Wallets:", self.wallets.keys())
            print("Active wallet:", active_wallet)
            print("Wallet name:", active_wallet[WalletKeys.NAME])
            
            if active_wallet:

                wallet_name = active_wallet[WalletKeys.NAME]

                if wallet_name in self.wallets:

                    self.switch_wallet(wallet_name)

                elif self.wallets:

                    first_wallet = next(iter(self.wallets))
                    self.switch_wallet(first_wallet)

                    self.logger.warning(
                        f"'{wallet_name}' not found. Switched to '{first_wallet}'."
                    )

            return True

        except Exception as e:

            self.logger.exception(e)

            return False

    # -----------------------------------------------------
    # Wallet Status
    # -----------------------------------------------------

    def is_connected(self) -> bool:

        return self.active_wallet is not None

    def has_wallet(self) -> bool:

        return len(self.wallets) > 0

    # -----------------------------------------------------
    # Active Wallet
    # -----------------------------------------------------

    def get_wallet(self) -> Wallet:

        if not self.active_wallet:

            raise RuntimeError(

                "No active wallet"

            )

        return self.wallets[self.active_wallet]

    def get_keypair(self) -> Keypair:

        return self.get_wallet().keypair

    def get_public_key(self) -> str:

        return str(

            self.get_wallet().public_key

        )


    # -----------------------------------------------------
    # Wallet Name
    # -----------------------------------------------------

    def get_wallet_name(self) -> str:

        return self.get_wallet().name
    # -----------------------------------------------------
    # Switch Wallet
    # -----------------------------------------------------

    def switch_wallet(self, wallet_name: str):

        if self.active_wallet == wallet_name:
            return

        if wallet_name not in self.wallets:
            raise ValueError(f"Wallet '{wallet_name}' not found")

        self.active_wallet = wallet_name

        self.logger.info(
            f"Active wallet -> {wallet_name}"
        )

    # -----------------------------------------------------
    # Wallet List
    # -----------------------------------------------------

    def get_wallet_names(self) -> list[str]:

        return list(self.wallets.keys())

    # -----------------------------------------------------
    # Remove Wallet
    # -----------------------------------------------------
    def remove_wallet(self, wallet_name: str):

        if wallet_name not in self.wallets:
            return

        del self.wallets[wallet_name]
        self.wallet_assets.pop(wallet_name, None)

        if self.active_wallet == wallet_name:

            self.active_wallet = None

            if self.wallets:
                self.active_wallet = next(iter(self.wallets))

        self.logger.info(
            f"Wallet removed -> {wallet_name}"
        )

        
    # -----------------------------------------------------
    # Disconnect_active_wallet
    # -----------------------------------------------------

    def disconnect_active_wallet(self):

        if not self.active_wallet:
            return

        wallet = self.get_wallet()

        wallet.connected = False

        self.logger.info(
            f"Active wallet ({wallet.name}) disconnected"
        )

        self.active_wallet = None

    # -----------------------------------------------------
    # Disconnect_all_wallets
    # -----------------------------------------------------

    def disconnect_all_wallets(self):

        for wallet in self.wallets.values():
            wallet.connected = False
            self.logger.info(
                f"All Wallet disconnected::Wallet {wallet.name} disconnected"
            )

     
        
        

        self.active_wallet = None



    # -----------------------------------------------------
    # Balance (Lamports)
    # -----------------------------------------------------

    async def get_balance(self) -> int:

        if not self.is_connected():
            return 0

        response = await self.client.get_balance(
            self.get_wallet().public_key
        )

        if response.value is None:
            return 0

        return response.value


    # -----------------------------------------------------
    # Balance (SOL)
    # -----------------------------------------------------

    async def get_sol_balance(self) -> float:

        lamports = await self.get_balance()

        return lamports / 1_000_000_000

    # -----------------------------------------------------
    # RPC Health
    # -----------------------------------------------------

    async def rpc_health(self) -> bool:

        try:

            await self.client.get_latest_blockhash()

            return True

        except Exception as e:

            self.logger.exception(e)

            return False

    # -----------------------------------------------------
    # Wallet Information
    # -----------------------------------------------------

    async def get_wallet_info(self) -> dict:

        if not self.is_connected():

            return {
                "connected": False,
                "wallet_name": "",
                "public_key": "",
                "balance": 0.0,
                "rpc_url": self.rpc_url
            }

        return {

            "connected": True,

            "wallet_name": self.get_wallet_name(),

            "public_key": self.get_public_key(),

            "balance": await self.get_sol_balance(),

            "rpc_url": self.rpc_url

        }


    # -----------------------------------------------------
    # Reconnect
    # -----------------------------------------------------

    def reconnect(self, config) -> bool:
        """
        اتصال مجدد از روی فایل تنظیمات
        """

        try:

            self.disconnect_all_wallet()

            return self.load_wallets_from_config(config)

        except Exception as e:

            self.logger.exception(e)

            return False

    # -----------------------------------------------------
    # RPC Connection Test
    # -----------------------------------------------------

    async def ping(self) -> bool:
        """
        تست اتصال RPC
        """

        try:

            await self.client.get_latest_blockhash()

            return True

        except Exception as e:

            self.logger.exception(e)

            return False

    # -----------------------------------------------------
    # Current Slot
    # -----------------------------------------------------

    async def get_current_slot(self) -> int:

        try:

            response = await self.client.get_slot()

            return response.value

        except Exception:

            return 0

    # -----------------------------------------------------
    # Latest Blockhash
    # -----------------------------------------------------

    async def get_latest_blockhash(self):

        return await self.client.get_latest_blockhash()

    # -----------------------------------------------------
    # Change RPC
    # -----------------------------------------------------

    async def reconnect_rpc(self, rpc_url: str):

        self.set_rpc_url(rpc_url)

        return await self.ping()

    # -----------------------------------------------------
    # Export Public Key
    # -----------------------------------------------------

    def export_public_key(self) -> str:

        if not self.is_connected():

            return ""

        return self.get_public_key()

    # -----------------------------------------------------
    # Export Wallet
    # -----------------------------------------------------

    def export_wallet(self) -> dict:

        if not self.is_connected():

            return {}

        wallet = self.get_wallet()

        return {

            "name": wallet.name,

            "public_key": str(wallet.public_key),

            "connected": wallet.connected

        }

    # -----------------------------------------------------
    # Clear Wallets
    # -----------------------------------------------------

    def clear(self):

        self.wallets.clear()

        self.wallet_assets.clear()

        self.active_wallet = None

        self.logger.info("Wallet list cleared")
    # -----------------------------------------------------
    # Wallet Count
    # -----------------------------------------------------

    @property
    def wallet_count(self) -> int:

        return len(self.wallets)

    # -----------------------------------------------------
    # Active Wallet Property
    # -----------------------------------------------------

    @property
    def active(self):

        if not self.is_connected():

            return None

        return self.get_wallet()
    # -----------------------------------------------------
    # String
    # -----------------------------------------------------

    def __str__(self):

        if not self.is_connected():

            return "WalletManager(Disconnected)"

        return (

            f"WalletManager("

            f"{self.get_wallet_name()}, "

            f"{self.get_public_key()}"

            f")"

        )

    # -----------------------------------------------------
    # Representation
    # -----------------------------------------------------

    def __repr__(self):

        return self.__str__()
    
    def get_wallet_by_name(self, wallet_name: str) -> Optional[Wallet]:
        return self.wallets.get(wallet_name)


    def get_public_key_by_name(self, wallet_name: str):

        wallet = self.get_wallet_by_name(wallet_name)

        if wallet is None:
            return None
        
        return str(wallet.public_key)
        
        
    def is_active_wallet(self, wallet_name: str):

        return wallet_name == self.active_wallet


    def set_wallet_assets(self,  wallet_name: str, assets: list)-> None:
        self.wallet_assets[wallet_name] = assets

    def get_wallet_assets(self, wallet_name: str) -> list:
        return self.wallet_assets.get(wallet_name, [])

    def clear_wallet_assets(self, wallet_name: str | None = None) -> None:
        if wallet_name is None:
            self.wallet_assets.clear()
        else:
            self.wallet_assets.pop(wallet_name, None) 

    def get_active_wallet_assets(self) -> list:
        """Return cached assets for active wallet."""

        if self.active_wallet is None:
            return []

        return self.wallet_assets.get(
            self.active_wallet,
            [],
        )