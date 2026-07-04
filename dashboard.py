"""
Dashboard
│
├── QTimer
│
└── refresh_all()
        │
        ├── await CurrentWalletWidget.refresh()
        ├── await PortfolioWidget.refresh()
        ├── await TradeWidget.refresh()
        └── await HistoryWidget.refresh()
"""


from PySide6.QtWidgets import (
     QMainWindow, QWidget,
    QTabWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QMessageBox, QHBoxLayout,
)

from gui.widgets.current_wallet_widget import CurrentWalletWidget
from gui.widgets.portfolio_widget import PortfolioWidget

from PySide6.QtCore import QTimer
from qasync import asyncSlot

from core.common.constants import UIConstants, WalletKeys

from core.common.logger import get_logger 

import asyncio


class Dashboard(QMainWindow):
    def __init__(
        self,
        service,
        wallet_manager,
        history,
        config,
    ):
        super().__init__()

    
        self.token_service = service
        self.history = history
        self.config = config
        self.wallet_manager = wallet_manager

        self.current_wallet_widget = None
        self.portfolio_widget = None

        self.logger = get_logger("dashboard")
 
        self._setup_window()        
        self._create_tabs()

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_all)
        self.refresh_timer.start(5000)

        QTimer.singleShot(0, self.refresh_all)


        

    def _setup_window(self):

        self.setWindowTitle("Token Trading Dashboard")
        self.setGeometry(UIConstants.WINDOW_lEFT, UIConstants.WINDO_TOP, UIConstants.WINDOW_WIDTH, UIConstants.WINDOW_HEIGHT)
    
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)



    def _create_tabs(self):

        self._init_wallet_tab()
        self._init_token_tab()
        self._init_trade_tab()
        self._init_liquidity_tab()
        self._init_staking_tab()
        self._init_history_tab()
        #self.refresh_wallet()

    # -------------------------
    # 1. WALLET TAB
    # -------------------------
    def _init_wallet_tab(self):
       
        self.current_wallet_widget = CurrentWalletWidget(
            self.wallet_manager,
            self.token_service
        )

        self.portfolio_widget = PortfolioWidget(
            self.wallet_manager,
            self.token_service
        )

        self.portfolio_widget.wallet_selected.connect(
            self.on_wallet_selected
        )
        tab = self._create_wallet_layout()

        self.tabs.addTab(tab, "Wallet")


    def _create_wallet_layout(self):
        
        tab = QWidget()

        layout = QHBoxLayout()

        layout.addWidget(
            self.current_wallet_widget,
            2
        )

        layout.addWidget(
            self.portfolio_widget,
            1
        )
        tab.setLayout(layout)

        return tab        



   
    # -------------------------
    # 2. Swith wallet
    # -------------------------  
    def switch_wallet(self):

        try:

            # پیدا کردن Wallet بعدی
            next_index = self.config.get_next_enabled_wallet_index()

            # ذخیره در Config
            self.config.set_active_wallet(next_index)

            # گرفتن Wallet فعال
            wallet = self.config.get_active_wallet()

            # تغییر Wallet فعال
            self.wallet_manager.switch_wallet(
                wallet[WalletKeys.NAME]
            )
            
            self.current_wallet_widget.refresh()
            self.portfolio_widget.load_assets()

            # بروزرسانی Dashboard
        #    self.refresh_wallet()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Switch Wallet",
                str(e)
            ) 
    
    def on_wallet_selected(self, wallet_name):
        
        self.wallet_manager.switch_wallet(wallet_name)
    
        print("Selected:", wallet_name)
        print("Active:", self.wallet_manager.get_active_wallet())
        #pass
        #self.wallet_changed.emit()

    # -------------------------
    # 2. TOKEN TAB
    # -------------------------
    def _init_token_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.token_name = QLineEdit()
        self.token_name.setPlaceholderText("Token Name")

        create_btn = QPushButton("Create Token")
        create_btn.clicked.connect(self.create_token)

        layout.addWidget(self.token_name)
        layout.addWidget(create_btn)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Token")

    def create_token(self):
        result = self.trading_service.create_token()
        self.history.add("create_token", result["status"], result.get("signature"))

    # -------------------------
    # 3. TRADE TAB
    # -------------------------
    def _init_trade_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.mint_input = QLineEdit()
        self.mint_input.setPlaceholderText("Token Mint")

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")

        buy_btn = QPushButton("Buy")
        sell_btn = QPushButton("Sell")

        buy_btn.clicked.connect(lambda: self.trade("buy"))
        sell_btn.clicked.connect(lambda: self.trade("sell"))

        layout.addWidget(self.mint_input)
        layout.addWidget(self.amount_input)
        layout.addWidget(buy_btn)
        layout.addWidget(sell_btn)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Trade")

    def trade(self, side):
        mint = self.mint_input.text()
        amount = int(self.amount_input.text())

        if side == "buy":
            result = self.trading_service.buy_token(mint, "self", amount)
        else:
            result = self.trading_service.sell_token(mint, "self", amount)

        self.history.add("trade", result["status"], result.get("signature"))

        self.refresh_all()

    # -------------------------
    # 4. LIQUIDITY TAB
    # -------------------------
    def _init_liquidity_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Liquidity Manager (Simple Mode)"))

        add_btn = QPushButton("Add Liquidity")
        add_btn.clicked.connect(self.add_liquidity)

        layout.addWidget(add_btn)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Liquidity")

    def add_liquidity(self):
        self.history.add("liquidity", "success")

    # -------------------------
    # 5. STAKING TAB
    # -------------------------
    def _init_staking_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        stake_btn = QPushButton("Stake Token")
        stake_btn.clicked.connect(self.stake)

        layout.addWidget(stake_btn)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Staking")

    def stake(self):
        self.trading_service.stake("demo", 100)
        self.history.add("stake", "success")

    # -------------------------
    # 6. HISTORY TAB
    # -------------------------
    def _init_history_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.history_box = QTextEdit()
        self.history_box.setReadOnly(True)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_history)

        layout.addWidget(self.history_box)
        layout.addWidget(refresh_btn)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "History")

    def load_history(self):
        data = self.history.get_all()
        text = "\n".join(str(tx) for tx in data)
        self.history_box.setText(text)
        
        if self.wallet_manager.is_connected():
            wallet_name = self.wallet_manager.get_wallet_name()
            pubkey = self.wallet_manager.get_public_key()
            
            
            # -------------------------
            #    balance 
            # -------------------------
            balance = "N/A"

            if hasattr(self.wallet_manager, "get_balance"):
                try:
                    #balance =  self.wallet_manager.get_balance()
                    balance = self.wallet_manager.get_balance_sync()
                    if balance is None:
                        balance = "0.000"
                    else:
                        balance = str(balance)

                except Exception:
                    balance = "N/A"
            
            self.logger.debug("BALANCE RAW: %s", balance)
            self.logger.debug("TYPE: %s", type(balance))
            # -------------------------

    def refresh_all(self):

        self.current_wallet_widget.refresh()

        self.portfolio_widget.load_assets()

        self.token_widget.refresh()

        self.history_widget.refresh()

    
    import asyncio



    @asyncSlot()
    async def refresh_all(self):

        tasks = []

        if hasattr(self, "current_wallet_widget"):
            tasks.append(self.current_wallet_widget.refresh())

        if hasattr(self, "portfolio_widget"):
            tasks.append(self.portfolio_widget.refresh())

        if hasattr(self, "trade_widget"):
            tasks.append(self.trade_widget.refresh())

        if hasattr(self, "history_widget"):
            tasks.append(self.history_widget.refresh())

        if tasks:
            await asyncio.gather(*tasks)
    

    @asyncSlot()
    async def refresh_all(self):

        if hasattr(self, "current_wallet_widget"):
            await self.current_wallet_widget.refresh()

        if hasattr(self, "portfolio_widget"):
            await self.portfolio_widget.refresh()

        if hasattr(self, "trade_widget"):
            await self.trade_widget.refresh()

        if hasattr(self, "history_widget"):
            await self.history_widget.refresh()

