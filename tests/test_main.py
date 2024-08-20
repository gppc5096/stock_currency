import unittest
from src.stock_currency import StockMonitorApp
from PyQt5.QtWidgets import QApplication


class TestStockMonitorApp(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.window = StockMonitorApp()

    def test_initial_setup(self):
        self.assertEqual(self.window.windowTitle(),
                         "USA Stock Currency Status")

    # 추가적인 테스트 케이스 작성


if __name__ == "__main__":
    unittest.main()
