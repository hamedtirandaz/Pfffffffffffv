"""
PortfolioWidget
    ├── refresh()      ← دریافت اطلاعات
    ├── update_tree()  ← نمایش
    ├── on_item_clicked()
    └── on_error()
"""


from PySide6.QtCore import Signal, QObject, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
)
 
 
class PortfolioWidget(QWidget):

    wallet_selected = Signal(str)

    def __init__(self, wallet_manager, token_service):

        super().__init__()

        self.wallet_manager = wallet_manager

        self.token_service = token_service

        self.tree = QTreeWidget()

        self.tree.setHeaderHidden(True)

        self.tree.itemClicked.connect(
            self.on_item_clicked
        )

        layout = QVBoxLayout()

        layout.addWidget(self.tree)

        self.setLayout(layout)

        

        self.item_to_wallet = {}



    # ==========================================================
    # PortfolioWidget
    # ==========================================================   
    
    def update_tree(self, wallets: dict):
   
        self.tree.clear()
        self.item_to_wallet.clear()
                 

        for wallet_name, assets in wallets.items():

            active = (
                wallet_name ==
                self.wallet_manager.get_wallet_name()
            )

            print("PORTFOLIO_WIDGET")

            if active:
            #    title = f"🟢 {wallet_name}   (Active)"
                title = f"{wallet_name}   (Active)"
            else:
                title = f"{wallet_name}"
#                title = f"⚪ {wallet_name}"

            wallet_item = QTreeWidgetItem([title])

            self.item_to_wallet[wallet_item] = wallet_name

                        
            wallet_item = QTreeWidgetItem([title])

            print("PORTFOLIO_WIDGET222")
            
            self.tree.addTopLevelItem(wallet_item)

            print(wallet_name, type(assets), assets)

            for asset in assets:

                symbol = asset["symbol"]

                amount = asset["amount"]

                if symbol == "SOL":
                    icon = "💰"
                elif symbol == "USDT":
                    icon = "💵"
                else:
                    icon = "🪙"

                child = QTreeWidgetItem(
                    [f"    {icon} {symbol:<8} {amount}"]
                )
                wallet_item.addChild(child)

        
            wallet_item.setExpanded(True)
        
            font = QFont()
            font.setBold(True)

            wallet_item.setFont(0, font)


        totals = {}

        for assets in wallets.values():

            for asset in assets:

                symbol = asset["symbol"]
                amount = asset["amount"]

                totals[symbol] = totals.get(symbol, 0) + amount


        total_item = QTreeWidgetItem(["📊 Totals"])

        font = QFont()
        font.setBold(True)

        total_item.setFont(0, font)

        self.tree.addTopLevelItem(total_item)

        for symbol, amount in totals.items():

            if symbol == "SOL":
                icon = "💰"
            elif symbol == "USDT":
                icon = "💵"
            else:
                icon = "🪙"

            total_item.addChild(
                QTreeWidgetItem(
                    [f"{icon} {symbol:<8} {amount}"]
                )
            )

        total_item.setExpanded(True)

    def on_item_clicked(self, item, column):

        if item.parent() is None:
            wallet_name = self.item_to_wallet[item]

            self.wallet_selected.emit(
               wallet_name
            )
            print(f"FFFFFFFFFFF item.text(0) {item.text(0)}::::wallet_name={wallet_name} ")

    def on_error(self, message: str):

        self.tree.clear()

        item = QTreeWidgetItem(
            [f"❌ {message}"]
        )

        self.tree.addTopLevelItem(item)

@asyncSlot()
async def refresh(self):

    try:

        wallets = await self.token_service.get_all_wallet_assets()

        self.update_tree(wallets)

    except Exception as e:

        self.on_error(str(e))