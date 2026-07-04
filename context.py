"""
==============================================================
Wizard Context (UI State Only)

این کلاس فقط وضعیت UI Wizard را نگه می‌دارد.
هیچ منطق بلاکچین یا RPC نباید داخل آن باشد.
==============================================================
"""

from dataclasses import dataclass, field
from typing import Optional, Dict


@dataclass
class WizardContext:

    # -------------------------------
    # Wallet UI state
    # -------------------------------
    active_wallet_name: str = ""
    wallet_public_key: str = ""

    # -------------------------------
    # Token form state
    # -------------------------------
    token_name: str = ""
    symbol: str = ""
    description: str = ""
    decimals: int = 9
    supply: int = 0
    image_path: str = ""

    # -------------------------------
    # Trade UI state
    # -------------------------------
    selected_mint: str = ""
    trade_amount: float = 0.0
    trade_side: str = ""   # buy / sell

    # -------------------------------
    # Staking UI state
    # -------------------------------
    stake_amount: float = 0.0

    # -------------------------------
    # Liquidity UI state
    # -------------------------------
    liquidity_token_amount: float = 0.0
    liquidity_sol_amount: float = 0.0

    # -------------------------------
    # UI runtime state
    # -------------------------------
    loading: bool = False
    last_error: str = ""
    last_result: dict = field(default_factory=dict)

    # -------------------------------
    # Notes / temporary UI data
    # -------------------------------
    notes: Dict = field(default_factory=dict)

    # -------------------------------
    # RESET (safe version)
    # -------------------------------
    def reset(self):
        for field_name in self.__dataclass_fields__:
            field_def = self.__dataclass_fields__[field_name]
            setattr(self, field_name, field_def.default if field_def.default != field(default_factory=dict) else {})