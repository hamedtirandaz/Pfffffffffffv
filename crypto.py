"""
==============================================================
crypto.py

توابع عمومی رمزنگاری

این فایل هیچ وابستگی به Solana، Wallet یا RPC ندارد.

وظایف:

✔ SHA256
✔ SHA512
✔ Base58
✔ Base64
✔ HEX
✔ Random Bytes
✔ Salt
✔ Token
✔ UUID
✔ Password Generator

Author:
Hamed Tirandaz
==============================================================
"""

from __future__ import annotations

import os
import uuid
import base64
import secrets
import hashlib

import base58


# ==========================================================
# SHA
# ==========================================================

def sha256(data: bytes | str) -> str:
    """
    محاسبه SHA256
    """

    if isinstance(data, str):
        data = data.encode("utf-8")

    return hashlib.sha256(data).hexdigest()


# ----------------------------------------------------------

def sha512(data: bytes | str) -> str:
    """
    محاسبه SHA512
    """

    if isinstance(data, str):
        data = data.encode("utf-8")

    return hashlib.sha512(data).hexdigest()


# ==========================================================
# Random
# ==========================================================

def random_bytes(length: int = 32) -> bytes:
    """
    تولید بایت تصادفی امن
    """

    return os.urandom(length)


# ----------------------------------------------------------

def random_hex(length: int = 32) -> str:
    """
    تولید رشته Hex تصادفی

    length بر حسب بایت است.
    """

    return random_bytes(length).hex()


# ----------------------------------------------------------

def random_token(length: int = 32) -> str:
    """
    تولید Token امن
    """

    return secrets.token_urlsafe(length)


# ----------------------------------------------------------

def random_uuid() -> str:
    """
    تولید UUID4
    """

    return str(uuid.uuid4())


# ----------------------------------------------------------

def generate_salt(length: int = 32) -> bytes:
    """
    تولید Salt
    """

    return os.urandom(length)


# ==========================================================
# Base64
# ==========================================================

def base64_encode(data: bytes | str) -> str:
    """
    Base64 Encode
    """

    if isinstance(data, str):
        data = data.encode("utf-8")

    return base64.b64encode(data).decode("utf-8")


# ----------------------------------------------------------

def base64_decode(data: str) -> bytes:
    """
    Base64 Decode
    """

    return base64.b64decode(data)


# ==========================================================
# Base58
# ==========================================================

def base58_encode(data: bytes | str) -> str:
    """
    Base58 Encode
    """

    if isinstance(data, str):
        data = data.encode("utf-8")

    return base58.b58encode(data).decode("utf-8")


# ----------------------------------------------------------

def base58_decode(data: str) -> bytes:
    """
    Base58 Decode
    """

    return base58.b58decode(data)


# ==========================================================
# HEX
# ==========================================================

def hex_encode(data: bytes | str) -> str:
    """
    تبدیل به Hex
    """

    if isinstance(data, str):
        data = data.encode("utf-8")

    return data.hex()


# ----------------------------------------------------------

def hex_decode(data: str) -> bytes:
    """
    تبدیل Hex به Bytes
    """

    return bytes.fromhex(data)


# ==========================================================
# Secure Compare
# ==========================================================

def secure_compare(value1: str,
                   value2: str) -> bool:
    """
    مقایسه امن دو رشته

    مقاوم در برابر Timing Attack
    """

    return secrets.compare_digest(
        value1,
        value2
    )


# ==========================================================
# Password
# ==========================================================

_PASSWORD_CHARS = (

    "abcdefghijklmnopqrstuvwxyz"

    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    "0123456789"

    "!@#$%^&*()-_=+"
)


def generate_password(length: int = 20) -> str:
    """
    تولید رمز عبور تصادفی
    """

    return "".join(

        secrets.choice(_PASSWORD_CHARS)

        for _ in range(length)

    )


# ==========================================================
# Entropy
# ==========================================================

def entropy_bits(byte_count: int) -> int:
    """
    محاسبه میزان Entropy

    هر بایت = 8 بیت
    """

    return byte_count * 8



# ==========================================================
# Cryptography
# ==========================================================

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

from cryptography.hazmat.primitives.kdf.pbkdf2 import (
    PBKDF2HMAC
)

from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.backends import default_backend


# ==========================================================
# Key Derivation
# ==========================================================

def derive_key(
    password: str,
    salt: bytes,
    iterations: int = 390000
) -> bytes:
    """
    تولید کلید رمزنگاری از Password
    """

    kdf = PBKDF2HMAC(

        algorithm=hashes.SHA256(),

        length=32,

        salt=salt,

        iterations=iterations,

        backend=default_backend()

    )

    key = kdf.derive(
        password.encode("utf-8")
    )

    return base64.urlsafe_b64encode(key)


# ==========================================================
# Password Hash
# ==========================================================

def password_hash(
    password: str,
    salt: bytes
) -> str:
    """
    Hash رمز عبور
    """

    key = derive_key(
        password,
        salt
    )

    return sha256(key)


# ==========================================================
# Encrypt
# ==========================================================

def encrypt_text(
    text: str,
    password: str,
    salt: bytes
) -> str:
    """
    رمزگذاری متن
    """

    key = derive_key(
        password,
        salt
    )

    cipher = Fernet(key)

    token = cipher.encrypt(
        text.encode("utf-8")
    )

    return token.decode("utf-8")


# ==========================================================
# Decrypt
# ==========================================================

def decrypt_text(
    encrypted: str,
    password: str,
    salt: bytes
) -> str:
    """
    رمزگشایی متن
    """

    key = derive_key(
        password,
        salt
    )

    cipher = Fernet(key)

    data = cipher.decrypt(
        encrypted.encode("utf-8")
    )

    return data.decode("utf-8")


# ==========================================================
# Safe Decrypt
# ==========================================================

def safe_decrypt(
    encrypted: str,
    password: str,
    salt: bytes
):
    """
    رمزگشایی بدون Exception
    """

    try:

        return True, decrypt_text(

            encrypted,

            password,

            salt

        )

    except InvalidToken:

        return False, "Invalid password."

    except Exception as exc:

        return False, str(exc)


# ==========================================================
# Verify Password
# ==========================================================

def verify_password(
    password: str,
    password_digest: str,
    salt: bytes
):
    """
    بررسی Password
    """

    current = password_hash(
        password,
        salt
    )

    return secure_compare(
        current,
        password_digest
    )


# ==========================================================
# Wallet Encryption
# ==========================================================

def encrypt_private_key(
    private_key: str,
    password: str
):
    """
    رمزگذاری Private Key

    خروجی:

    encrypted_key

    salt
    """

    salt = generate_salt()

    encrypted = encrypt_text(

        private_key,

        password,

        salt

    )

    return encrypted, base64_encode(salt)


# ----------------------------------------------------------

def decrypt_private_key(
    encrypted_key: str,
    password: str,
    salt: str
):
    """
    بازیابی Private Key
    """

    salt = base64_decode(salt)

    return safe_decrypt(

        encrypted_key,

        password,

        salt

    )