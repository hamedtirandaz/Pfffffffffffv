import logging
import sys
from pathlib import Path
from datetime import datetime


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


# ---------- حذف فایل‌های قدیمی ----------

MAX_LOG_FILES = 3

log_files = sorted(
    LOG_DIR.glob("app_*.log"),
    key=lambda f: f.stat().st_mtime
)

while len(log_files) >= MAX_LOG_FILES:
    log_files[0].unlink()
    log_files.pop(0)


# ---------- فایل لاگ این اجرا ----------

log_name = datetime.now().strftime(
    "app_%Y-%m-%d_%H-%M-%S.log"
)

LOG_FILE = LOG_DIR / log_name


def get_logger(name: str = "PumpFun") -> logging.Logger:

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter(
         # "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
         "[%(asctime)s] "
         "[%(levelname)s] "
         "%(name)s.%(funcName)s:%(lineno)d - "
         "%(message)s"
    )

    # Console

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)

    # File

    file = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    file.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file)

    logger.info("=" * 70)
    logger.info("Application started")
    logger.info(f"Log file: {LOG_FILE.name}")

    return logger