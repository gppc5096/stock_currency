from stock_currency import StockMonitorApp
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = StockMonitorApp()
    ex.show()
    sys.exit(app.exec_())
