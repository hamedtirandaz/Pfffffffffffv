"""
==========================================================
PumpFun AMM Manager
Application Entry Point
==========================================================
"""

import os
import sys
import asyncio
import traceback
from pathlib import Path

os.system("cls" if os.name == "nt" else "clear")

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ----------------------------------------------------------
# Qt
# ----------------------------------------------------------

from PySide6.QtWidgets import QApplication, QMessageBox

# ----------------------------------------------------------
# qasync
# ----------------------------------------------------------

from qasync import QEventLoop

# ----------------------------------------------------------
# Config
# ----------------------------------------------------------

from config import Config

# ----------------------------------------------------------
# Core
# ----------------------------------------------------------

from core.common.logger import get_logger
from core.wallet import WalletManager
from core.services import TokenService
from core.history.transaction_history import TransactionHistory

# ----------------------------------------------------------
# GUI
# ----------------------------------------------------------

from gui.dashboard import Dashboard
from gui.style import load_stylesheet


logger = get_logger("main")

logger.info("=" * 60)
logger.info("PumpFun AMM Manager starting...")
logger.info(f"Python : {sys.version}")
logger.info(f"Working directory : {os.getcwd()}")
logger.info(f"Project root : {PROJECT_ROOT}")


# ==========================================================
# Exception Handler
# ==========================================================

def exception_hook(exc_type, exc_value, exc_traceback):

    error_text = "".join(
        traceback.format_exception(
            exc_type,
            exc_value,
            exc_traceback
        )
    )

    logger.critical(
        "Unhandled exception",
        exc_info=(exc_type, exc_value, exc_traceback),
    )

    app = QApplication.instance()

    if app:
        QMessageBox.critical(
            None,
            "Unexpected Error",
            error_text
        )
    else:
        print(error_text)


# ==========================================================
# QApplication
# ==========================================================

def create_application():

    logger.info("Creating QApplication")

    app = QApplication(sys.argv)

    app.setApplicationName(
        "PumpFun AMM Manager"
    )

    stylesheet = load_stylesheet()

    if stylesheet:
        app.setStyleSheet(stylesheet)

    return app


# ==========================================================
# Config
# ==========================================================

def load_config():

    logger.info("Loading config")

    config = Config()
    config.load()

    return config


# ==========================================================
# Wallet
# ==========================================================

def build_wallet(config):

    logger.info("Initializing wallet")

    wallet_manager = WalletManager(
        rpc_url=config.get("rpc_url")
    )

    try:
        wallet_manager.load_wallets_from_config(config)
        logger.info("Wallets loaded successfully")

    except Exception:
        logger.exception("Failed to load wallets")

    return wallet_manager


# ==========================================================
# Services
# ==========================================================

def build_services(config, wallet_manager):

    logger.info("Building services")

    history = TransactionHistory()

    token_service = TokenService(
        wallet_manager
    )

    logger.info("Services initialized")

    return {

        "wallet": wallet_manager,
        "history": history,
        "token": token_service,

    }


# ==========================================================
# Main
# ==========================================================

async def main(app: QApplication):

    sys.excepthook = exception_hook

    config = load_config()

    wallet_manager = build_wallet(config)

    if wallet_manager.is_connected():

        logger.info(
            "Wallet : %s",
            wallet_manager.get_public_key()
        )

    else:

        logger.warning(
            "Application started without wallet"
        )

    services = build_services(
        config,
        wallet_manager
    )

    window = Dashboard(
        service=services["token"],
        wallet_manager=wallet_manager,
        history=services["history"],
        config=config,
    )

    window.show()

    logger.info("Application started")

    # نگه داشتن Coroutine اصلی زنده
    await asyncio.Event().wait()


# ==========================================================

if __name__ == "__main__":

    app = create_application()

    loop = QEventLoop(app)

    asyncio.set_event_loop(loop)

    sys.excepthook = exception_hook

    try:

        with loop:
            loop.run_until_complete(main(app))

    finally:

        logger.info("Application closed")