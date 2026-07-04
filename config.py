"""
=========================================================
config.py

مدیریت تنظیمات برنامه

وظایف این فایل:

1- خواندن تنظیمات از config.json
2- ایجاد فایل تنظیمات در اولین اجرا
3- ذخیره تنظیمات
4- تغییر مقدار هر تنظیم
5- دریافت مقدار هر تنظیم
=========================================================
"""
 

 

import json
from pathlib import Path
from core.common.constants import WalletKeys
from core.helpers import project_root

from core.common.logger import get_logger   # اضافه کردن ایمپورت

logger = get_logger()           # ساخت یک logger محلی


class Config:
    """
    کلاس مدیریت تنظیمات برنامه

    تمام تنظیمات برنامه داخل این کلاس نگهداری می‌شوند.
    """

    # --------------------------------------------------
    # سازنده کلاس
    # --------------------------------------------------
    def __init__(self, file_name=None):

        if file_name is None:
            self.file_path = project_root() / "config" / "config.json"
        else:
            self.file_path = Path(file_name)
    
         # دیکشنری تنظیمات
        self.data = {}

    # --------------------------------------------------
    # تنظیمات پیشفرض
    # --------------------------------------------------
    def default_config(self) -> dict:
        """
        اگر فایل config.json وجود نداشته باشد،
        این تنظیمات ساخته می‌شوند.
        """

        return {

            # RPC سولانا
            "rpc_url": "https://api.mainnet-beta.solana.com",

            # شبکه
            "network": "mainnet",

            # مسیر کیف پول
            "wallet_path": "",

            # کلید خصوصی
            #?????  بعدا بهتر است کلید خصوصی را با رمزنگاری مخفی نمایم
            "private_key": "",

            # Priority Fee
            "priority_fee": 10000,

            # Slippage
            "slippage": 5,

            # فعال بودن لاگ
            "enable_logs": True,

            # حالت تیره
            "dark_mode": True,

            # زبان برنامه
            "language": "fa",
            
            # Future AMM / bot flags
            "auto_trading": False,
            "risk_limit": 0.1,

        }

    # --------------------------------------------------
    # بارگذاری تنظیمات
    # --------------------------------------------------
    def load(self)-> None:
        """
        خواندن فایل تنظیمات
        """

        # اگر فایل وجود نداشت
        if not self.file_path.exists():
            logger.warning("Config file not found: %s", self.file_path)
            #print("Config file not found.")

            self.data = self.default_config()

            self.save()

            return

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                self.data = json.load(file)
            # merge missing keys (important upgrade)
            self._merge_defaults()

        except Exception as error:
             # ثبت خطا به همراه جزئیات کامل (traceback)
            logger.exception(
                "Error loading config file, %s",
                error
            )
            #print("Error loading config:")
            #print(error)

            # اگر فایل خراب باشد
            # تنظیمات پیشفرض ساخته می‌شود.
            self.data = self.default_config()

            self.save()

    # --------------------------------------------------
    def _merge_defaults(self):
        """
        Adds missing keys from default config
        (prevents crash after updates)
        """

        defaults = self.default_config()

        updated = False

        for key, value in defaults.items():
            if key not in self.data:
                self.data[key] = value
                updated = True

        if updated:
            logger.info("Config updated with missing default keys")
            self.save()
    
    
    # --------------------------------------------------
    # ذخیره تنظیمات
    # --------------------------------------------------
    def save(self)-> None:
        """
        ذخیره تنظیمات داخل فایل
        """

        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)

        except Exception as e:
            logger.exception("Failed to save config: %s", e)

    # --------------------------------------------------
    # گرفتن مقدار یک تنظیم
    # --------------------------------------------------
    def get(self, key, default=None):

        return self.data.get(key, default)

    # --------------------------------------------------
    # تغییر مقدار یک تنظیم
    # --------------------------------------------------
    def set(self, key: str, value)-> None:

        self.data[key] = value

    # --------------------------------------------------
    # حذف یک تنظیم
    # --------------------------------------------------
    def remove(self, key: str)-> None:
        self.data.pop(key, None)

    # --------------------------------------------------
    # بررسی وجود یک تنظیم
    # --------------------------------------------------
    def contains(self, key: str) -> bool:

        return key in self.data

    # --------------------------------------------------
    # برگرداندن کل تنظیمات
    # --------------------------------------------------
    def all(self) -> dict:

        return self.data

    # --------------------------------------------------
    # ریست تنظیمات
    # --------------------------------------------------
    def reset(self)-> None:

        self.data = self.default_config()

        self.save()

    # --------------------------------------------------
    # نمایش تنظیمات
    # --------------------------------------------------
    def __str__(self)-> None:

        return json.dumps(
            self.data,
            indent=4,
            ensure_ascii=False
        )

    # --------------------------------------------------
    # Active Wallet
    # --------------------------------------------------
    def get_active_wallet(self) -> dict:
        index = self.data["active_wallet_index"]
        return self.data["wallets"][index]

    # --------------------------------------------------
    # Active Wallet--Index
    # --------------------------------------------------
    def get_active_wallet_index(self) -> int:
        return self.data["active_wallet_index"]

    

    # --------------------------------------------------
    # All Wallet
    # --------------------------------------------------
    def get_wallets(self) -> list:
        return self.data["wallets"]
    
    # --------------------------------------------------
    # Activated Wallets
    # --------------------------------------------------
    def get_enabled_wallets(self) -> list:
        return [
            wallet
            for wallet in self.data["wallets"]
            if wallet.get("enabled", True)
        ]
    
    # --------------------------------------------------
    # Change Active Wallet
    # --------------------------------------------------
    def set_active_wallet(self, index: int):
        self.data["active_wallet_index"] = index
        self.save()

    # --------------------------------------------------
    # Active Wallet---Private Key
    # --------------------------------------------------
    def get_active_private_key(self) -> str:
        return self.get_active_wallet()["private_key"]

    # --------------------------------------------------
    # Activate Wallet--Name
    # --------------------------------------------------
    def get_active_wallet_name(self) -> str:
        return self.get_active_wallet()["name"]

    # --------------------------------------------------
    # All Tokens
    # --------------------------------------------------
    def get_watch_tokens(self) -> list:
        return self.data["watch_tokens"]

    # --------------------------------------------------
    # All Activated Tokens
    # --------------------------------------------------
    def get_enabled_watch_tokens(self) -> list:
        return [
            token
            for token in self.data["watch_tokens"]
            if token.get("enabled", True)
        ]

    # --------------------------------------------------
    # All Traded Tokens
    # --------------------------------------------------
    def get_trading_tokens(self) -> list:
        return [
            token
            for token in self.get_enabled_watch_tokens()
            if token["role"] == "trading"
        ]


    # --------------------------------------------------
    # Assets Tokens
    # --------------------------------------------------
    def get_asset_tokens(self) -> list:
        return [
            token
            for token in self.get_enabled_watch_tokens()
            if token["role"] == "asset"
        ]


    # --------------------------------------------------
    # Next Wallet Index
    # --------------------------------------------------
    def get_next_enabled_wallet_index(self) -> int:
        """
        Return the index of the next enabled wallet.
        """

        wallets = self.get_wallets()

        if not wallets:
            return 0

        current = self.get_active_wallet_index()
        count = len(wallets)

        for i in range(1, count + 1):
            index = (current + i) % count

            if wallets[index].get(WalletKeys.ENABLED, True):
                return index

        return None