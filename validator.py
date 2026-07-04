"""
==============================================================
validator.py

اعتبارسنجی داده‌های ورودی برنامه

وظایف:

✔ اعتبارسنجی نام توکن
✔ اعتبارسنجی Symbol
✔ اعتبارسنجی Supply
✔ اعتبارسنجی Decimals
✔ اعتبارسنجی RPC URL
✔ اعتبارسنجی Private Key
✔ اعتبارسنجی Public Key
✔ اعتبارسنجی Slippage
✔ اعتبارسنجی Priority Fee

این فایل هیچ وابستگی به رابط کاربری ندارد.

Author:
Hamed Tirandaz
==============================================================
"""

import re
from urllib.parse import urlparse

import base58


class Validator:
    """
    کلاس اعتبارسنجی
    """

    # --------------------------------------------------
    # Token Name
    # --------------------------------------------------

    @staticmethod
    def validate_token_name(name: str):

        name = name.strip()

        if not name:
            return False, "نام توکن وارد نشده است."

        if len(name) < 2:
            return False, "نام توکن حداقل باید ۲ کاراکتر باشد."

        if len(name) > 32:
            return False, "نام توکن نباید بیشتر از ۳۲ کاراکتر باشد."

        return True, ""

    # --------------------------------------------------
    # Symbol
    # --------------------------------------------------

    @staticmethod
    def validate_symbol(symbol: str):

        symbol = symbol.strip().upper()

        if not symbol:
            return False, "نماد توکن وارد نشده است."

        if len(symbol) > 10:
            return False, "نماد توکن نباید بیشتر از ۱۰ کاراکتر باشد."

        if not re.fullmatch(r"[A-Z0-9]+", symbol):
            return False, "نماد فقط می‌تواند شامل حروف انگلیسی و عدد باشد."

        return True, ""

    # --------------------------------------------------
    # Decimals
    # --------------------------------------------------

    @staticmethod
    def validate_decimals(value):

        try:
            value = int(value)
        except Exception:
            return False, "Decimals باید عدد صحیح باشد."

        if value < 0 or value > 9:
            return False, "Decimals باید بین 0 تا 9 باشد."

        return True, ""

    # --------------------------------------------------
    # Supply
    # --------------------------------------------------

    @staticmethod
    def validate_supply(value):

        try:
            value = int(value)
        except Exception:
            return False, "Supply باید عدد صحیح باشد."

        if value <= 0:
            return False, "Supply باید بزرگ‌تر از صفر باشد."

        return True, ""

    # --------------------------------------------------
    # RPC URL
    # --------------------------------------------------

    @staticmethod
    def validate_rpc_url(url: str):

        url = url.strip()

        if not url:
            return False, "آدرس RPC وارد نشده است."

        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return False, "RPC باید با http یا https شروع شود."

        if not parsed.netloc:
            return False, "آدرس RPC معتبر نیست."

        return True, ""

    # --------------------------------------------------
    # Slippage
    # --------------------------------------------------

    @staticmethod
    def validate_slippage(value):

        try:
            value = float(value)
        except Exception:
            return False, "Slippage معتبر نیست."

        if value < 0:
            return False, "Slippage نمی‌تواند منفی باشد."

        if value > 100:
            return False, "Slippage نباید بیشتر از 100 باشد."

        return True, ""

    # --------------------------------------------------
    # Priority Fee
    # --------------------------------------------------

    @staticmethod
    def validate_priority_fee(value):

        try:
            value = int(value)
        except Exception:
            return False, "Priority Fee معتبر نیست."

        if value < 0:
            return False, "Priority Fee نمی‌تواند منفی باشد."

        return True, ""

    # --------------------------------------------------
    # Base58
    # --------------------------------------------------

    @staticmethod
    def validate_base58(value: str):

        try:
            base58.b58decode(value)

            return True, ""

        except Exception:

            return False, "رشته Base58 معتبر نیست."

    # --------------------------------------------------
    # Public Key
    # --------------------------------------------------

    @staticmethod
    def validate_public_key(value: str):

        ok, message = Validator.validate_base58(value)

        if not ok:
            return False, message

        if len(value) < 32:
            return False, "Public Key معتبر نیست."

        return True, ""

    # --------------------------------------------------
    # Private Key
    # --------------------------------------------------

    @staticmethod
    def validate_private_key(value: str):

        ok, message = Validator.validate_base58(value)

        if not ok:
            return False, message

        try:

            decoded = base58.b58decode(value)

        except Exception:

            return False, "Private Key معتبر نیست."

        if len(decoded) not in (32, 64):
            return False, "طول Private Key معتبر نیست."

        return True, ""

    # --------------------------------------------------
    # Empty
    # --------------------------------------------------

    @staticmethod
    def validate_required(value, title="مقدار"):

        if value is None:
            return False, f"{title} وارد نشده است."

        if isinstance(value, str):

            if not value.strip():
                return False, f"{title} وارد نشده است."

        return True, ""

    # --------------------------------------------------
    # عدد مثبت
    # --------------------------------------------------

    @staticmethod
    def validate_positive_number(value, title="عدد"):

        try:

            value = float(value)

        except Exception:

            return False, f"{title} معتبر نیست."

        if value <= 0:

            return False, f"{title} باید بزرگ‌تر از صفر باشد."

        return True, ""

    # --------------------------------------------------
    # بازه عددی
    # --------------------------------------------------

    @staticmethod
    def validate_range(value, minimum, maximum, title="مقدار"):

        try:

            value = float(value)

        except Exception:

            return False, f"{title} معتبر نیست."

        if value < minimum:

            return False, f"{title} نباید کمتر از {minimum} باشد."

        if value > maximum:

            return False, f"{title} نباید بیشتر از {maximum} باشد."

        return True, ""