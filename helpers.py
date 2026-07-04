"""
==============================================================
helpers.py

توابع عمومی مورد استفاده در کل پروژه

این فایل شامل توابعی است که:

✔ وابسته به GUI نیستند
✔ وابسته به Wallet نیستند
✔ وابسته به RPC نیستند
✔ وابسته به Solana SDK نیستند

Author:
Hamed Tirandaz

==============================================================
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Any


# ==========================================================
# File & Directory
# ==========================================================

def ensure_directory(path: str | Path) -> Path:
    """
    ایجاد پوشه در صورت نبودن

    Parameters
    ----------
    path : str | Path

    Returns
    -------
    Path
    """

    directory = Path(path)

    directory.mkdir(
        parents=True,
        exist_ok=True
    )

    return directory


# ----------------------------------------------------------

def ensure_parent_directory(file_path: str | Path) -> Path:
    """
    ایجاد پوشه والد فایل
    """

    file_path = Path(file_path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return file_path


# ==========================================================
# JSON
# ==========================================================

def load_json(file_path: str | Path,
              default: Any = None) -> Any:
    """
    خواندن فایل JSON

    اگر فایل وجود نداشت یا خراب بود،
    مقدار default برگردانده می‌شود.
    """

    file_path = Path(file_path)

    if not file_path.exists():

        return default

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return default


# ----------------------------------------------------------

def save_json(file_path: str | Path,
              data: Any,
              indent: int = 4):
    """
    ذخیره فایل JSON
    """

    file_path = ensure_parent_directory(file_path)

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(

            data,

            f,

            indent=indent,

            ensure_ascii=False

        )


# ==========================================================
# Time
# ==========================================================

def now() -> datetime:
    """
    زمان فعلی
    """

    return datetime.now()


# ----------------------------------------------------------

def timestamp() -> int:
    """
    Unix Timestamp
    """

    return int(
        datetime.now().timestamp()
    )


# ----------------------------------------------------------

def datetime_string(
        fmt="%Y-%m-%d %H:%M:%S"):
    """
    رشته زمان
    """

    return datetime.now().strftime(fmt)


# ==========================================================
# UUID
# ==========================================================

def generate_uuid():
    """
    تولید UUID
    """

    return str(
        uuid.uuid4()
    )


# ==========================================================
# File Size
# ==========================================================

def human_size(size: int):
    """
    تبدیل حجم فایل

    مثال

    1024

    →

    1.00 KB
    """

    units = [

        "B",

        "KB",

        "MB",

        "GB",

        "TB"

    ]

    size = float(size)

    for unit in units:

        if size < 1024:

            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


# ==========================================================
# SOL
# ==========================================================

LAMPORTS_PER_SOL = 1_000_000_000


def sol_to_lamports(sol: float):
    """
    SOL

    →

    Lamports
    """

    return int(

        sol *

        LAMPORTS_PER_SOL

    )


# ----------------------------------------------------------

def lamports_to_sol(lamports: int):
    """
    Lamports

    →

    SOL
    """

    return (

        lamports /

        LAMPORTS_PER_SOL

    )


# ==========================================================
# Paths
# ==========================================================

def project_root() -> Path:
    """
    مسیر ریشه پروژه
    """
 
    return Path(__file__).resolve().parent.parent

# ----------------------------------------------------------

def config_dir() -> Path:
    return project_root() / "config"




def logs_directory():
    """
    پوشه Log
    """

    return ensure_directory(

        project_root() /

        "logs"

    )


# ----------------------------------------------------------

def config_directory():
    """
    پوشه Config
    """

    return ensure_directory(

        project_root() /

        "config"

    )


# ----------------------------------------------------------

def assets_directory() -> Path:
    """
    پوشه Assets
    """

    return ensure_directory(

        project_root() /

        "assets"

    )

def config_file() -> Path:
    return config_dir() / "config.json"

# ----------------------------------------------------------

def styles_directory():
    """
    پوشه Style
    """

    return ensure_directory(

        assets_directory() /

        "styles"

    )


# ----------------------------------------------------------

def images_directory():
    """
    پوشه تصاویر
    """

    return ensure_directory(

        assets_directory() /

        "images"

    )

# ==========================================================
# String Helpers
# ==========================================================

def is_empty(value) -> bool:
    """
    بررسی خالی بودن مقدار
    """

    if value is None:
        return True

    if isinstance(value, str):
        return value.strip() == ""

    return False


# ----------------------------------------------------------

def safe_strip(value):
    """
    حذف فاصله‌های ابتدا و انتهای رشته

    اگر مقدار رشته نباشد، بدون تغییر برگردانده می‌شود.
    """

    if isinstance(value, str):
        return value.strip()

    return value


# ----------------------------------------------------------

def truncate(text: str,
             length: int = 50):
    """
    کوتاه کردن متن
    """

    if text is None:
        return ""

    if len(text) <= length:
        return text

    return text[:length] + "..."


# ----------------------------------------------------------

def shorten_address(address: str):
    """
    کوتاه کردن آدرس سولانا

    Example

    ABCDEFGHIJKLMNOPQRSTUVWXYZ

    →

    ABCD...WXYZ
    """

    if not address:

        return ""

    if len(address) <= 12:

        return address

    return f"{address[:4]}...{address[-4:]}"


# ==========================================================
# Number Helpers
# ==========================================================

def clamp(value,
          minimum,
          maximum):
    """
    محدود کردن مقدار
    """

    return max(
        minimum,
        min(
            value,
            maximum
        )
    )


# ----------------------------------------------------------

def safe_int(value,
             default=0):
    """
    تبدیل امن به int
    """

    try:

        return int(value)

    except Exception:

        return default


# ----------------------------------------------------------

def safe_float(value,
               default=0.0):
    """
    تبدیل امن به float
    """

    try:

        return float(value)

    except Exception:

        return default


# ==========================================================
# Collection Helpers
# ==========================================================

def chunk_list(data,
               chunk_size):
    """
    تقسیم لیست به چند قسمت

    Example

    [1,2,3,4,5]

    →

    [[1,2],[3,4],[5]]
    """

    for i in range(
        0,
        len(data),
        chunk_size
    ):

        yield data[
            i:i+chunk_size
        ]


# ----------------------------------------------------------

def unique(items):
    """
    حذف موارد تکراری
    """

    return list(
        dict.fromkeys(items)
    )


# ==========================================================
# Retry
# ==========================================================

def retry(function,
          retries=3,
          exceptions=(Exception,),
          *args,
          **kwargs):
    """
    اجرای مجدد تابع
    """

    last_error = None

    for _ in range(retries):

        try:

            return function(
                *args,
                **kwargs
            )

        except exceptions as exc:

            last_error = exc

    raise last_error


# ==========================================================
# Dictionary
# ==========================================================

def deep_get(dictionary,
             keys,
             default=None):
    """
    خواندن مقدار از دیکشنری تو در تو

    Example

    deep_get(
        data,
        ["rpc","timeout"]
    )
    """

    value = dictionary

    for key in keys:

        if not isinstance(
            value,
            dict
        ):

            return default

        if key not in value:

            return default

        value = value[key]

    return value


# ==========================================================
# File Helpers
# ==========================================================

def file_exists(path):
    """
    وجود فایل
    """

    return Path(path).exists()


# ----------------------------------------------------------

def delete_file(path):
    """
    حذف فایل
    """

    path = Path(path)

    if path.exists():

        path.unlink()


# ==========================================================
# Misc
# ==========================================================

def noop(*args,
         **kwargs):
    """
    تابع بدون عملیات

    برای Callbackهای موقت
    """

    pass


# ----------------------------------------------------------

def identity(value):
    """
    مقدار را بدون تغییر برمی‌گرداند.
    """

    return value


# ----------------------------------------------------------

def bool_to_yes_no(value):
    """
    True

    →

    Yes

    False

    →

    No
    """

    return "Yes" if value else "No"


# ----------------------------------------------------------

def bool_to_enabled(value):
    """
    True

    →

    Enabled

    False

    →

    Disabled
    """

    return "Enabled" if value else "Disabled"