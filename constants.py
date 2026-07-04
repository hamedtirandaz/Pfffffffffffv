"""
==============================================================
constants.py

تعریف تمام ثابت‌های مورد نیاز برنامه به صورت دسته‌بندی‌شده

در این فایل تمام مقادیر ثابت برنامه نگهداری می‌شوند.

مزایا:
    ✔ خوانایی بیشتر
    ✔ جلوگیری از تکرار مقادیر
    ✔ تغییر آسان تنظیمات
    ✔ توسعه راحت‌تر پروژه
==============================================================
"""

APP_NAME = "Pump.fun AMM Manager"
APP_VERSION = "0.1.0"
APP_AUTHOR = "Hamed Tirandaz"

# ==========================================================
# اطلاعات کلی برنامه
# ==========================================================
class AppConstants:
    """اطلاعات شناسایی برنامه"""

    NAME = APP_NAME
    VERSION = APP_VERSION
    AUTHOR = APP_AUTHOR

    WINDOW_TITLE = f"{NAME} v{VERSION}"


# ==========================================================
# تنظیمات رابط کاربری
# ==========================================================
class UIConstants:
    """ابعاد و اندازه‌های پنجره"""

    
    WINDOW_WIDTH = 900

    WINDOW_HEIGHT = 600
    
    WINDO_TOP = 60
    
    WINDOW_lEFT = 210

    MIN_WIDTH = 700

    MIN_HEIGHT = 700
    REFRESH_INTERVAL = 5000   # ms


# ==========================================================
# مسیر فایل‌ها
# ==========================================================
class PathConstants:
    """مسیر فایل‌های پروژه"""
    """مسیر فایل‌های پیکربندی، لاگ، استایل و آیکون"""

    CONFIG_FILE = "config.json"

    LOG_FILE = "logs/app.log"

    STYLE_DARK = "assets/style/dark.qss"

    STYLE_LIGHT = "assets/style/light.qss"

    ICON = "assets/icon.ico"


# ==========================================================
# شبکه‌های سولانا
# ==========================================================
class RPCConstants:
    """آدرس RPC شبکه‌های سولانا"""

    MAINNET = "https://api.mainnet-beta.solana.com"

    DEVNET = "https://api.devnet.solana.com"

    TESTNET = "https://api.testnet.solana.com"

    DEFAULT = MAINNET   # RPC پیش‌فرض

    TIMEOUT = 30
    COMMITMENT = "confirmed"

    MAX_RETRIES = 3

# ==========================================================
# نام شبکه‌ها (برای استفاده در تنظیمات)
# ==========================================================
class NetworkConstants:
    """نام شبکه‌های قابل انتخاب"""

    MAINNET = "mainnet"
    DEVNET = "devnet"
    TESTNET = "testnet"
    DEFAULT = MAINNET


# ==========================================================
# تنظیمات کیف پول
# ==========================================================
class WalletConstants:
    """محدودیت‌ها و مقادیر پیش‌فرض مربوط به کیف پول و تراکنش"""

    DEFAULT_SLIPPAGE = 5.0

    DEFAULT_PRIORITY_FEE = 10000

    MAX_SLIPPAGE = 100

    MIN_SLIPPAGE = 0

    MAX_PRIORITY_FEE = 1_000_000

    MIN_PRIORITY_FEE = 0


# ==========================================================
# Transaction
# ==========================================================

class TransactionConstants:

    LAMPORTS_PER_SOL = 1_000_000_000

    DEFAULT_COMPUTE_UNIT_LIMIT = 200_000

    DEFAULT_COMPUTE_UNIT_PRICE = 10_000


# ==========================================================
# تایم‌اوت‌های مختلف
# ==========================================================
class TimeoutConstants:
    """زمان‌های انتظار برای عملیات مختلف (بر حسب ثانیه)"""

    RPC = 30
    TRANSACTION = 60
    CONFIRM = 120
    
    


# ==========================================================
# عملیات برنامه
# ==========================================================
class TaskConstants:

    CREATE_TOKEN = "Create Token"

    CREATE_POOL = "Create Pool"

    BUY = "Buy"

    SELL = "Sell"

    BURN = "Burn"
    SWAP = "Swap"


# ==========================================================
# وضعیت Worker ها
# ==========================================================
class WorkerConstants:

    READY = "Ready"

    RUNNING = "Running"

    FINISHED = "Finished"

    FAILED = "Failed"
    CANCELLED = "Cancelled"


# ==========================================================
# تنظیمات Logger
# ==========================================================
class LoggerConstants:

    DEBUG = "DEBUG"

    INFO = "INFO"

    WARNING = "WARNING"

    ERROR = "ERROR"

    CRITICAL = "CRITICAL"

    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


# ==========================================================
# رنگ‌های لاگ
# ==========================================================
class ColorConstants:

    INFO = "#00C853"

    WARNING = "#FFD600"

    ERROR = "#D50000"

    DEBUG = "#29B6F6"


# ==========================================================
# فیلتر فایل‌ها
# ==========================================================
class FileDialogConstants:
    """الگوهای فیلتر برای کادرهای باز/ذخیره فایل"""

    JSON = "JSON Files (*.json)"

    TEXT = "Text Files (*.txt)"

    ALL = "All Files (*.*)"


# ==========================================================
# پیام‌های عمومی
# ==========================================================
class MessageConstants:
    """متون قابل نمایش به کاربر (ترجیحاً به زبان فارسی)"""

    SUCCESS = "عملیات با موفقیت انجام شد."

    FAILED = "عملیات با خطا مواجه شد."

    LOADING = "در حال بارگذاری..."

    CONNECTING = "در حال اتصال به شبکه..."

    WAIT = "لطفاً منتظر بمانید..."

    INVALID_PRIVATE_KEY = "کلید خصوصی معتبر نیست."

    RPC_ERROR = "خطا در ارتباط با RPC."

    WALLET_NOT_CONNECTED = "کیف پول متصل نیست."

    BALANCE_UPDATED = "موجودی با موفقیت به‌روزرسانی شد."

    SETTINGS_SAVED = "تنظیمات ذخیره شد."

class WizardPages:
    WELCOME = 0
    WALLET = 1
    RPC = 2
    SETTINGS = 3
    TRADING = 4    


class TokenRole:
    ASSET = "asset"
    TRADING = "trading"

class WalletKeys:
    NAME = "name"
    PRIVATE_KEY = "private_key"
    ENABLED = "enabled"
    