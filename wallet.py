"""
==============================================================
wallet.py

مدیریت کیف پول برنامه

این کلاس تنها نقطه دسترسی سایر بخش‌های پروژه
به کیف پول است.

وظایف:

✔ نگهداری اطلاعات کیف پول
✔ بارگذاری از فایل
✔ ذخیره در فایل
✔ آماده برای اتصال به RPC
✔ آماده برای امضای تراکنش
✔ آماده برای رمزگذاری کلید خصوصی

Author:
Hamed Tirandaz
==============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from core.common.logger import get_logger

logger = get_logger()


# ==========================================================
# Wallet
# ==========================================================

@dataclass
class Wallet:
    """
    مدل کیف پول

    توجه:
    این کلاس فقط API اصلی را تعریف می‌کند.
    پیاده‌سازی عملیات حساس (مانند تولید کلید،
    امضا و ...) در مراحل بعد تکمیل خواهد شد.
    """

    # آدرس عمومی کیف پول
    address: str = ""

    # کلید خصوصی (در حافظه)
    _private_key: Optional[str] = None

    # نام فایل ذخیره شده
    file_path: Optional[Path] = None

    # وضعیت بارگذاری
    loaded: bool = False

    # ------------------------------------------------------

    @classmethod
    def generate(cls) -> "Wallet":
        """
        ایجاد یک کیف پول جدید.

        پیاده‌سازی تولید واقعی کلیدها
        در نسخه بعدی انجام خواهد شد.
        """

        logger.info("Generate wallet requested.")

        raise NotImplementedError(
            "Wallet generation is not implemented yet."
        )

    # ------------------------------------------------------

    @classmethod
    def from_private_key(
        cls,
        private_key: str
    ) -> "Wallet":
        """
        ساخت کیف پول از روی کلید خصوصی.
        """

        logger.info("Import wallet from private key.")

        raise NotImplementedError(
            "Import from private key is not implemented yet."
        )

    # ------------------------------------------------------

    @classmethod
    def from_file(
        cls,
        path: str | Path,
        password: Optional[str] = None
    ) -> "Wallet":
        """
        بارگذاری کیف پول از فایل.
        """

        logger.info(f"Loading wallet: {path}")

        raise NotImplementedError(
            "Loading wallet is not implemented yet."
        )

    # ------------------------------------------------------

    def save(
        self,
        path: str | Path,
        password: Optional[str] = None
    ) -> None:
        """
        ذخیره کیف پول در فایل.
        """

        logger.info(f"Saving wallet: {path}")

        raise NotImplementedError(
            "Saving wallet is not implemented yet."
        )

    # ------------------------------------------------------

    @property
    def private_key(self) -> Optional[str]:
        """
        دسترسی فقط-خواندنی به کلید خصوصی.
        """

        return self._private_key

    # ------------------------------------------------------

    @property
    def is_loaded(self) -> bool:
        """
        آیا کیف پول آماده استفاده است؟
        """

        return self.loaded

    # ------------------------------------------------------

    def clear(self) -> None:
        """
        پاک کردن اطلاعات حساس از حافظه.
        """

        logger.info("Clearing wallet from memory.")

        self._private_key = None
        self.address = ""
        self.file_path = None
        self.loaded = False

    # ------------------------------------------------------

    def sign_message(self, message: bytes) -> bytes:
        """
        امضای پیام.

        در نسخه بعدی تکمیل می‌شود.
        """

        raise NotImplementedError(
            "Message signing is not implemented yet."
        )

    # ------------------------------------------------------

    def get_balance(self) -> float:
        """
        دریافت موجودی کیف پول.

        این متد در نسخه بعدی از RpcManager
        استفاده خواهد کرد.
        """

        raise NotImplementedError(
            "Balance retrieval is not implemented yet."
        )

    # ------------------------------------------------------

    def __repr__(self) -> str:
        """
        نمایش خلاصه کیف پول.
        """

        return (
            f"Wallet("
            f"address='{self.address}', "
            f"loaded={self.loaded})"
        )


# ==========================================================
# Wallet Status
# ==========================================================

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any


class WalletStatus(Enum):
    """
    وضعیت کیف پول
    """

    EMPTY = "empty"
    LOADED = "loaded"
    LOCKED = "locked"
    ERROR = "error"


# ==========================================================
# Wallet Metadata
# ==========================================================

@dataclass
class WalletMetadata:
    """
    اطلاعات جانبی کیف پول
    """

    name: str = ""
    description: str = ""

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    last_opened: Optional[datetime] = None

    tags: list[str] = field(
        default_factory=list
    )


# ==========================================================
# Wallet Extensions
# ==========================================================

class Wallet:

    # ------------------------------------------------------

    @property
    def status(self) -> WalletStatus:

        if self.loaded:

            return WalletStatus.LOADED

        return WalletStatus.EMPTY

    # ------------------------------------------------------

    @property
    def has_private_key(self):

        return self._private_key is not None

    # ------------------------------------------------------

    def lock(self):
        """
        حذف اطلاعات حساس از حافظه
        """

        logger.info("Wallet locked.")

        self._private_key = None

        self.loaded = False

    # ------------------------------------------------------

    def unlock(
        self,
        password: Optional[str] = None
    ):
        """
        باز کردن کیف پول

        در نسخه بعدی تکمیل خواهد شد.
        """

        raise NotImplementedError

    # ------------------------------------------------------

    def refresh(self):
        """
        بروزرسانی اطلاعات کیف پول

        بعداً موجودی، nonce و...
        از RpcManager خوانده می‌شود.
        """

        logger.info(
            "Refreshing wallet."
        )

    # ------------------------------------------------------

    def balance(self):

        return self.get_balance()

    # ------------------------------------------------------

    def exists(self):

        return self.loaded

    # ------------------------------------------------------

    def export_public_data(self):

        """
        اطلاعات قابل نمایش
        """

        return {

            "address": self.address,

            "loaded": self.loaded,

            "status": self.status.value

        }

    # ------------------------------------------------------

    def import_metadata(
        self,
        metadata: WalletMetadata
    ):

        self.metadata = metadata

    # ------------------------------------------------------

    def export_metadata(self):

        return getattr(
            self,
            "metadata",
            WalletMetadata()
        )

    # ------------------------------------------------------

    def rpc(self):

        """
        در نسخه بعدی:

        return RpcManager(...)
        """

        raise NotImplementedError

    # ------------------------------------------------------

    def validate(self):

        """
        اعتبارسنجی اولیه وضعیت کیف پول
        """

        if not self.address:

            return False

        return True

    # ------------------------------------------------------

    def close(self):

        """
        پایان کار با کیف پول
        """

        logger.info(
            "Wallet closed."
        )

        self.clear()

    # ------------------------------------------------------

    def __bool__(self):

        return self.loaded


# ==========================================================
# Wallet Serialization & State
# ==========================================================

from dataclasses import asdict
from datetime import datetime
from typing import Dict, Any


class Wallet:

    # ------------------------------------------------------
    # وضعیت‌های کمکی
    # ------------------------------------------------------

    def is_ready(self) -> bool:
        """
        آیا کیف پول آماده استفاده است؟
        """

        return (
            self.loaded
            and bool(self.address)
        )

    # ------------------------------------------------------

    def is_empty(self) -> bool:
        """
        آیا هیچ کیف پولی بارگذاری نشده است؟
        """

        return not self.loaded

    # ------------------------------------------------------

    def touch(self):
        """
        ثبت آخرین زمان استفاده
        """

        if hasattr(self, "metadata"):
            self.metadata.last_opened = datetime.utcnow()

    # ------------------------------------------------------

    def display_name(self) -> str:
        """
        نام نمایشی کیف پول
        """

        if hasattr(self, "metadata"):

            if self.metadata.name:

                return self.metadata.name

        return self.address[:8] + "..." if self.address else "No Wallet"

    # ------------------------------------------------------
    # Export
    # ------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        فقط اطلاعات عمومی کیف پول را برمی‌گرداند.
        """

        data = {
            "address": self.address,
            "loaded": self.loaded,
            "status": self.status.value,
        }

        if hasattr(self, "metadata"):
            data["metadata"] = asdict(self.metadata)

        return data

    # ------------------------------------------------------

    def to_json(self) -> Dict[str, Any]:
        """
        معادل JSON اطلاعات عمومی.
        """

        return self.to_dict()

    # ------------------------------------------------------
    # Metadata
    # ------------------------------------------------------

    def set_name(self, name: str):
        """
        تنظیم نام کیف پول
        """

        if not hasattr(self, "metadata"):
            self.metadata = WalletMetadata()

        self.metadata.name = name.strip()

    # ------------------------------------------------------

    def set_description(self, text: str):
        """
        تنظیم توضیحات
        """

        if not hasattr(self, "metadata"):
            self.metadata = WalletMetadata()

        self.metadata.description = text.strip()

    # ------------------------------------------------------

    def add_tag(self, tag: str):
        """
        افزودن برچسب
        """

        if not hasattr(self, "metadata"):
            self.metadata = WalletMetadata()

        tag = tag.strip()

        if tag and tag not in self.metadata.tags:
            self.metadata.tags.append(tag)

    # ------------------------------------------------------

    def remove_tag(self, tag: str):
        """
        حذف برچسب
        """

        if hasattr(self, "metadata"):

            if tag in self.metadata.tags:

                self.metadata.tags.remove(tag)

    # ------------------------------------------------------
    # Cache
    # ------------------------------------------------------

    def set_cached_balance(self, value: float):
        """
        ذخیره موجودی Cache
        """

        self._cached_balance = value
        self._cached_at = datetime.utcnow()

    # ------------------------------------------------------

    def cached_balance(self):
        """
        دریافت موجودی Cache
        """

        return getattr(self, "_cached_balance", None)

    # ------------------------------------------------------

    def cached_time(self):
        """
        زمان آخرین بروزرسانی Cache
        """

        return getattr(self, "_cached_at", None)

    # ------------------------------------------------------
    # Reset
    # ------------------------------------------------------

    def reset(self):
        """
        بازگرداندن شیء به وضعیت اولیه
        """

        self.clear()

        if hasattr(self, "metadata"):
            self.metadata = WalletMetadata()

    # ------------------------------------------------------

    def __str__(self):
        return self.display_name()