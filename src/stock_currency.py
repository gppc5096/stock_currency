import sys
import json
import yfinance as yf
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QWidget, QHeaderView, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PyQt5.QtGui import QPalette, QColor, QFont


class StockMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 창 제목 설정
        self.setWindowTitle('USA Stock Currency Status')

        # 창 크기 설정
        self.setGeometry(100, 100, 800, 800)

        # 창을 모니터 중앙에 배치
        self.center()

        # 메인 레이아웃 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # stock index 애니메이션 섹션 추가
        self.index_label = QLabel('', self)
        self.index_label.setFixedHeight(30)  # 높이 설정
        self.index_label.setFixedWidth(1000)  # 넓이 설정 (필요시 조정)

        # 스타일시트를 통해 폰트 크기 설정
        self.index_label.setStyleSheet("font-size: 15pt; color: RED;")

        main_layout.addWidget(self.index_label)

        # 지수 데이터 업데이트 및 애니메이션 시작
        self.update_index_data()

        # 타이틀 라벨 추가
        title_label = QLabel('USA Stock Currency Status', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20pt;")
        main_layout.addWidget(title_label)

        # 입력 필드와 라벨을 한 줄로 배열
        input_layout = QHBoxLayout()
        self.ticker_label = QLabel('틱커명:', self)
        self.ticker_input = QLineEdit(self)
        self.ticker_input.setPlaceholderText('e.g., AAPL')
        self.ticker_input.textChanged.connect(
            self.on_ticker_input_changed)  # 대문자 변환
        self.ticker_input.returnPressed.connect(
            self.add_data)  # 엔터를 누르면 데이터 추가

        self.one_year_label = QLabel('1년전 주가:', self)
        self.one_year_input = QLineEdit(self)
        self.one_year_input.textChanged.connect(
            self.on_price_input_changed)  # 달러 기호 추가

        self.six_month_label = QLabel('6개월전 주가:', self)
        self.six_month_input = QLineEdit(self)
        self.six_month_input.textChanged.connect(
            self.on_price_input_changed)  # 달러 기호 추가

        self.current_price_label = QLabel('현재 주가:', self)
        self.current_price_input = QLineEdit(self)
        self.current_price_input.textChanged.connect(
            self.on_price_input_changed)  # 달러 기호 추가

        input_layout.addWidget(self.ticker_label)
        input_layout.addWidget(self.ticker_input)
        input_layout.addWidget(self.one_year_label)
        input_layout.addWidget(self.one_year_input)
        input_layout.addWidget(self.six_month_label)
        input_layout.addWidget(self.six_month_input)
        input_layout.addWidget(self.current_price_label)
        input_layout.addWidget(self.current_price_input)

        main_layout.addLayout(input_layout)

        # 버튼 배열을 입력 필드 아래로 이동
        button_layout = QHBoxLayout()
        self.add_button = QPushButton('추가', self)
        self.update_button = QPushButton('수정', self)
        self.delete_button = QPushButton('삭제', self)
        self.reset_button = QPushButton('초기화', self)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.reset_button)

        main_layout.addLayout(button_layout)

        # 리스트 테이블 설정
        self.table = QTableWidget(self)
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ['틱커명', '1년전 주가', '6개월전 주가', '현재 주가'])

        # 헤더 크기 조정 모드 설정 (모든 헤더가 창 크기와 연동되도록 설정)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # 테이블 클릭 이벤트 연결
        self.table.cellClicked.connect(self.on_table_click)

        main_layout.addWidget(self.table)

        # 인용구 박스 추가
        quote_label = QLabel('made by 나종춘(2024)', self)
        quote_label.setAlignment(Qt.AlignRight)
        quote_label.setStyleSheet("font-size: 10pt;")
        main_layout.addWidget(quote_label)

        # 버튼 기능 연결
        self.add_button.clicked.connect(self.add_data)
        self.update_button.clicked.connect(self.update_data)
        self.delete_button.clicked.connect(self.delete_data)
        self.reset_button.clicked.connect(self.reset_fields)

        # JSON 파일 불러오기
        self.load_data()

        # 스타일시트 적용
        self.apply_styles()

    def center(self):
        # 창을 모니터 중앙에 위치시키는 함수
        qr = self.frameGeometry()
        cp = QApplication.desktop().screen().rect().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def update_index_data(self):
        # 지수 데이터 가져오기
        sp500 = yf.Ticker('^GSPC').history(period='1d')['Close'].iloc[-1]
        nasdaq100 = yf.Ticker('^NDX').history(period='1d')['Close'].iloc[-1]
        dow30 = yf.Ticker('^DJI').history(period='1d')['Close'].iloc[-1]

        # 텍스트 업데이트 및 항목 간 간격 조절
        self.index_label.setText(f'S&P500: {sp500:.2f}   |   NASDAQ100: {
                                 nasdaq100:.2f}   |   DOW30: {dow30:.2f}')

        # 애니메이션 설정
        self.index_animation = QPropertyAnimation(
            self.index_label, b"geometry")
        self.index_animation.setDuration(30000)  # 애니메이션 속도 조절 (10,000ms = 10초)
        self.index_animation.setStartValue(QRect(800, 10, 800, 30))
        self.index_animation.setEndValue(QRect(-800, 10, 800, 30))
        self.index_animation.setLoopCount(-1)  # 무한 반복
        self.index_animation.start()

        # 일정 시간마다 업데이트 (예: 60초마다)
        QTimer.singleShot(60000, self.update_index_data)

    def on_ticker_input_changed(self):
        # 틱커명을 대문자로 변환 및 주가 정보 가져오기
        text = self.ticker_input.text().upper()
        self.ticker_input.setText(text)
        if len(text) >= 1:  # 최소한 1글자 이상 입력된 경우에만 실행
            self.fetch_stock_data(text)

    def on_price_input_changed(self):
        # 입력된 가격 앞에 달러 기호 추가
        sender = self.sender()
        text = sender.text()
        if text and not text.startswith('$'):
            sender.setText(f'${text}')

    def fetch_stock_data(self, ticker):
        try:
            # yfinance 모듈을 사용하여 주식 데이터 가져오기
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")

            # 1년 전, 6개월 전, 현재 주가 계산
            if not hist.empty:
                one_year_ago_price = hist['Close'].iloc[0]  # 1년 전 주가
                six_month_ago_price = hist['Close'].iloc[len(
                    hist)//2]  # 약 6개월 전 주가
                current_price = hist['Close'].iloc[-1]  # 현재 주가

                self.one_year_input.setText(f"${one_year_ago_price:.2f}")
                self.six_month_input.setText(f"${six_month_ago_price:.2f}")
                self.current_price_input.setText(f"${current_price:.2f}")
            else:
                print("Error: No data found for ticker")

        except Exception as e:
            print("Error fetching stock data:", e)

    def add_data(self):
        # 틱커명 입력 여부 확인
        if not self.ticker_input.text():
            self.show_message("틱커명을 입력하세요.")
            return

        # 테이블에 새로운 행 추가
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        self.table.setItem(row_position, 0, QTableWidgetItem(
            self.ticker_input.text()))

        one_year_item = QTableWidgetItem(self.one_year_input.text())
        one_year_item.setTextAlignment(Qt.AlignRight)
        self.table.setItem(row_position, 1, one_year_item)

        six_month_item = QTableWidgetItem(self.six_month_input.text())
        six_month_item.setTextAlignment(Qt.AlignRight)
        self.table.setItem(row_position, 2, six_month_item)

        current_price_item = QTableWidgetItem(self.current_price_input.text())
        current_price_item.setTextAlignment(Qt.AlignRight)
        self.table.setItem(row_position, 3, current_price_item)

        # 데이터 저장
        self.save_data()

        # 필드 초기화
        self.reset_fields()

    def on_table_click(self, row, column):
        # 클릭한 행의 데이터를 입력 필드로 가져오기
        self.ticker_input.setText(self.table.item(row, 0).text())
        self.one_year_input.setText(self.table.item(row, 1).text())
        self.six_month_input.setText(self.table.item(row, 2).text())
        self.current_price_input.setText(self.table.item(row, 3).text())

    def update_data(self):
        # 선택된 행의 데이터를 업데이트
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.setItem(selected_row, 0, QTableWidgetItem(
                self.ticker_input.text()))

            one_year_item = QTableWidgetItem(self.one_year_input.text())
            one_year_item.setTextAlignment(Qt.AlignRight)
            self.table.setItem(selected_row, 1, one_year_item)

            six_month_item = QTableWidgetItem(self.six_month_input.text())
            six_month_item.setTextAlignment(Qt.AlignRight)
            self.table.setItem(selected_row, 2, six_month_item)

            current_price_item = QTableWidgetItem(
                self.current_price_input.text())
            current_price_item.setTextAlignment(Qt.AlignRight)
            self.table.setItem(selected_row, 3, current_price_item)

            # 데이터 저장
            self.save_data()

            # 필드 초기화
            self.reset_fields()

    def delete_data(self):
        # 선택된 행 삭제
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.removeRow(selected_row)

            # 데이터 저장
            self.save_data()

            # 필드 초기화
            self.reset_fields()

    def reset_fields(self):
        # 입력 필드 초기화
        self.ticker_input.clear()
        self.one_year_input.clear()
        self.six_month_input.clear()
        self.current_price_input.clear()

    def save_data(self):
        # 데이터를 JSON 파일로 저장
        data_list = []
        for row in range(self.table.rowCount()):
            row_data = {
                "ticker": self.table.item(row, 0).text(),
                "one_year_price": self.table.item(row, 1).text(),
                "six_month_price": self.table.item(row, 2).text(),
                "current_price": self.table.item(row, 3).text()
            }
            data_list.append(row_data)

        with open("stock_data.json", "w") as json_file:
            json.dump(data_list, json_file, indent=4)

    def load_data(self):
        # JSON 파일에서 데이터를 불러와 테이블에 추가
        try:
            with open("stock_data.json", "r") as json_file:
                data_list = json.load(json_file)
                for row_data in data_list:
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)

                    ticker_item = QTableWidgetItem(row_data["ticker"])
                    self.table.setItem(row_position, 0, ticker_item)

                    one_year_item = QTableWidgetItem(
                        row_data["one_year_price"])
                    one_year_item.setTextAlignment(Qt.AlignRight)
                    self.table.setItem(row_position, 1, one_year_item)

                    six_month_item = QTableWidgetItem(
                        row_data["six_month_price"])
                    six_month_item.setTextAlignment(Qt.AlignRight)
                    self.table.setItem(row_position, 2, six_month_item)

                    current_price_item = QTableWidgetItem(
                        row_data["current_price"])
                    current_price_item.setTextAlignment(Qt.AlignRight)
                    self.table.setItem(row_position, 3, current_price_item)
        except (FileNotFoundError, json.JSONDecodeError):
            # 파일이 없거나 JSONDecodeError가 발생하면 빈 리스트로 초기화
            print("No data found or JSON decode error. Starting with an empty table.")

    def apply_styles(self):
        # CSS 스타일 적용
        self.setStyleSheet("""
            QWidget {
                font-family: '맑은 고딕';
                font-size: 9pt;
            }
            QLabel {
                font-size: 9pt;
            }
            QLineEdit {
                font-size: 9pt;
                padding: 5px;
                height: 30px;
            }
            QPushButton {
                background-color: #dfeef7;
                padding: 10px;
                font-size: 9pt;
            }
            QTableWidget {
                font-size: 9pt;
            }
            QHeaderView::section {
                background-color: #abaaa7;
                color: white;
                padding: 5px;
                font-size: 9pt;
            }
        """)

    def show_message(self, message):
        # 메시지 박스를 이용해 팝업창을 띄움
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("입력 오류")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StockMonitorApp()
    ex.show()
    sys.exit(app.exec_())
