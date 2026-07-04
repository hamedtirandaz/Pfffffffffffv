# ==========================================================
# settings_page.py
# تنظیمات اصلی برنامه (RPC / Wallet / General Settings)
# ==========================================================

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout,
    QGroupBox, QLineEdit, QPushButton,
    QLabel, QMessageBox
)

from core.common.constants import RPCConstants
from core.common.logger import get_logger

logger = get_logger()


class SettingsPage(QWidget):
    """
    صفحه تنظیمات برنامه
    - تغییر RPC
    - مشاهده وضعیت اتصال
    """

    def __init__(self, config, rpc=None, parent=None):
        super().__init__(parent)

        self.config = config
        self.rpc = rpc

        self.init_ui()
        self.load_settings()

    # ------------------------------------------------------
    def init_ui(self):
        layout = QVBoxLayout(self)

        # ================= RPC SETTINGS =================
        rpc_group = QGroupBox("RPC Settings")
        form = QFormLayout()

        self.rpc_input = QLineEdit()
        self.rpc_input.setPlaceholderText("https://api.mainnet-beta.solana.com")

        self.status_label = QLabel("Unknown")

        form.addRow("RPC URL:", self.rpc_input)
        form.addRow("Status:", self.status_label)

        rpc_group.setLayout(form)

        # ================= BUTTONS =================
        self.btn_save = QPushButton("Save Settings")
        self.btn_test = QPushButton("Test RPC")

        self.btn_save.clicked.connect(self.save_settings)
        self.btn_test.clicked.connect(self.test_rpc)

        layout.addWidget(rpc_group)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_test)

        layout.addStretch()

    # ------------------------------------------------------
    def load_settings(self):
        """لود تنظیمات ذخیره‌شده"""
        rpc_url = self.config.get("rpc_url", RPCConstants.DEFAULT)
        self.rpc_input.setText(rpc_url)

        self.status_label.setText("Not tested")

    # ------------------------------------------------------
    def save_settings(self):
        """ذخیره تنظیمات"""
        rpc_url = self.rpc_input.text().strip()

        if not rpc_url:
            QMessageBox.warning(self, "Error", "RPC URL cannot be empty")
            return

        self.config.set("rpc_url", rpc_url)
        self.config.save()

        logger.info("RPC updated: %s", rpc_url)

        QMessageBox.information(self, "Saved", "Settings saved successfully")

    # ------------------------------------------------------
    def test_rpc(self):
        """تست اتصال RPC"""
        try:
            if not self.rpc:
                QMessageBox.warning(self, "Error", "RPC instance not provided")
                return

            # تست ساده: گرفتن blockhash
            blockhash = self.rpc.get_latest_blockhash()

            self.status_label.setText("Connected")
            self.status_label.setStyleSheet("color: green;")

            QMessageBox.information(
                self,
                "Success",
                f"RPC OK\nBlockhash: {blockhash[:10]}..."
            )

        except Exception as e:
            self.status_label.setText("Failed")
            self.status_label.setStyleSheet("color: red;")

            QMessageBox.critical(self, "RPC Error", str(e))

            logger.exception("RPC test failed: %s", e)