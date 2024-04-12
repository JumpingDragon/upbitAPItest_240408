import sys
import time
# delay 없으면 밴 당함

import requests
import pyupbit  # pip install pyupbit

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon

import telegram
import asyncio


form_class = uic.loadUiType("ui/upbitInfo.ui")[0]


# 시그널 클래스> 업비트 서버에 요청을 넣어서 코인 정보를 가져오는 일을 하는 클래스
class UpbitSignal(QThread):
    # 시그널 함수 선언(정의)
    coinDataSent = pyqtSignal(float, float, float, float, float, float, float, float)
    alarmDatasent = pyqtSignal(float)  # 현재가 하나만 가지는 시그널 함수 선언 (알람 용)

    def __init__(self, ticker):
        # 시그널 클래스 객체가 선언될 때 메인 윈도우에서 코인 종류를 받아오게 설계
        super().__init__()
        self.ticker = ticker  # 외부에서 받아온 매개변수를 전역변수로 사용.
        self.alive = True

    def run(self):
        while self.alive:  # 무한루프
            url = "https://api.upbit.com/v1/ticker"
            param = {"markets": f"KRW-{self.ticker}"}
            # 이와 동일: "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
            response = requests.get(url, params=param)

            result = response.json()

            trade_price = result[0]["trade_price"]  # 비트 코인의 현재가격
            high_price = result[0]["high_price"]  # 비트 코인의 최고가
            low_price = result[0]["low_price"]  # 비트 코인의 최저가
            closing_price = result[0]["prev_closing_price"]  # 비트 코인의 전일종가
            trade_vol = result[0]["trade_volume"]  # 비트 코인의 최근 거래량
            trade_vol_24 = result[0]["acc_trade_volume_24h"]  # 비트 코인의 24시간 누적 거래량
            trade_price_24 = result[0]["acc_trade_price_24h"]  # 비트 코인의 24시간 누적 거래대금
            change_rate = result[0]["signed_change_rate"]  # 비트 코인의 부호가 있는 변화율. +면 증가, -면 감소

            # 메인 윈도우 클래스로 받아온 데이터를 전송
            self.coinDataSent.emit(
                float(trade_price), float(high_price),
                float(low_price), float(closing_price),
                float(trade_vol), float(trade_vol_24),
                float(trade_price_24), float(change_rate)
            )
            self.alarmDatasent.emit(  # 알람용 현재가만 메인 윈도우에 보내주는 시그널 함수
                float(trade_price)
            )
            # 업비트 api 호출 딜레이 3초
            time.sleep(3)

    def close(self):
        self.alive = False


class MainWindow(QMainWindow, form_class):  # 슬롯 클래스
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # ui 불러오기
        self.setWindowTitle("비트코인 정보 프로그램 v2.0")
        self.setWindowIcon((QIcon("icon/bitcoin.png")))
        self.statusBar().showMessage("Upbit api Application v0.9")

        self.ticker = "BTC"

        self.ubs = UpbitSignal(self.ticker)  # 시그널 클래스로 객체 선언
        self.ubs.coinDataSent.connect(self.fillCoinData)
        self.ubs.coinDataSent.connect(self.alarmDetect)
        self.ubs.start()  # 시그널 클래스 run() 실행
        self.comboBox_setting()  # 콤보 박스 초기화 설정 함수 호출
        self.coin_comboBox.currentIndexChanged.connect(self.coin_comboBox_selected)
        # 콤보 박스의 메뉴 선택 변경 이벤트 발생 시 호출될 함수를 설정함.
        self.alarmBtn.clicked.connect(self.alarmButtonAction)

    def comboBox_setting(self):  # 코인리스트 콤보박스 설정 함수
        tickerList = pyupbit.get_tickers(fiat="KRW")  # 코인 종류(ticker list) 가져오기
        coinList = []
        # KRW- 를 제거한 텍스트를 리스트로 생성
        for ticker in tickerList:
            coinList.append(ticker[4:])
        coinList.remove("BTC")  # 리스트에서 btc 제거
        coinList = sorted(coinList)  # abc 순 오름차순으로 정렬
        coinList = ["BTC"] + coinList  # BTC 첫번째 순서가 되고 나머지 리스트는 정렬된 상태로 추가됨
        self.coin_comboBox.addItems(coinList)

    def coin_comboBox_selected(self):  # 콤보박스에서 새로운 코인 종류가 선택되었을 때 호출함수
        selected_ticker = self.coin_comboBox.currentText()  # 콤보박스에서 선택된 메뉴의 텍스트 가져오기
        self.ticker = selected_ticker

        self.coin_ticker_label.setText(self.ticker)
        self.ubs.close()  # while 문의 무한루프가 stop함수, 무한루프가 stop
        # 새로운 티커를 넣어서 새로운 시그널 객체를 생성.
        self.ubs = UpbitSignal(self.ticker)  # 시그널 클래스로 객체 선언
        self.ubs.coinDataSent.connect(self.fillCoinData)
        self.ubs.coinDataSent.connect(self.alarmDetect) # 이걸 안 적으면 매도와 매수 알람기능이 작동안됨.
        self.ubs.start()  # 시그널 클래스 run() 실행

    def fillCoinData(self, a, b, c, d, e, f, g, h):
        if a <= 1000:  # 천 원 미만인 애들은 소수점 첫째자리까지 나타내주자.
            self.trade_price.setText(f"{a: ,.1f}원")  # trade_price는 ui에 있는 레이블 이름
        else:
            self.trade_price.setText(f"{a: ,.0f}원")  # trade_price는 ui에 있는 레이블 이름
        self.high_price.setText(f"{b:,.0f}원")
        self.low_price.setText(f"{c:,.0f}원")
        self.closing_price.setText(f"{d:,.0f}원")
        self.trade_vol.setText(f"{e:,.3f}개")
        self.trade_vol_24.setText(f"{f:,.3f}개")
        self.trade_price_24.setText(f"{g:,.0f}원")
        self.change_rate.setText(f"{h:.2f}%")
        self.update_style()

    def alarmButtonAction(self):  # 알람 버튼 제어 함수
        self.alarmFlag = 0
        if self.alarmBtn.text() == "알람시작":
            self.alarmBtn.setText("알람중지")
        else:
            self.alarmBtn.setText("알람시작")

    def alarmDetect(self, trade_price):
        if self.alarmBtn.text() == "알람중지":
            sellPrice = float(self.alarmPrice1.text())  # 사용자가 입력한 매도목표가격
            buyPrice = float(self.alarmPrice2.text())  # 사용자가 입력한 매수목표가격

            # 현재 코인 가격이 사용자가 설정해 놓은 매도 가격보다 높아지면 매도 알람!
            if sellPrice <= trade_price:  # 팔 때는 비싼 값에 팔고
                if self.alarmFlag == 0:
                    print("매도가격 도달!! 매도하세요!!")
                    self.telegram_message(f"코인의 현재 가격이 {trade_price}원이 되었습니다!")
                    self.telegram_message(f"지정해놓은 {sellPrice}원 이상입니다. 매도하세요!")
                    self.alarmFlag = 1

            if buyPrice >= trade_price:  # 살 때는 싸게 사자
                if self.alarmFlag == 0:
                    print("매수가격 도달!! 매수하세요!!")
                    self.telegram_message(f"코인의 현재 가격이 {trade_price}원이 되었습니다!")
                    self.telegram_message(f"지정해놓은 {buyPrice}원 이상입니다. 매수하세요!")
                    self.alarmFlag = 1
        else:
            pass

    def update_style(self):  # 변화율이 +이면 빨간색, - 이면 파란색으로 표시
        if "-" in self.change_rate.text():
            self.change_rate.setStyleSheet("background-color:blue;color:white;border:(0,0,218);")
            self.trade_price.setStyleSheet("color:blue;")
        else:
            self.change_rate.setStyleSheet("background-color:red;color:white;border:(218,0,0);")
            self.trade_price.setStyleSheet("color:red;")

    def telegram_message(self, message): # 텔레그램에 메시지 전송해주는 함수
        bot = telegram.Bot(token="본인 텔레그램 토큰")
        chat_id = "본인 텔레그램 chat id"

        asyncio.run(bot.sendMessage(chat_id=chat_id, text=message))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
