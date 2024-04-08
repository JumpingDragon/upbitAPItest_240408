import sys
import time
# delay 없으면 밴 당함

import requests

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("ui/testUI.ui")[0]

# 시그널 클래스> 업비트 서버에 요청을 넣어서 코인 정보를 가져오는 일을 하는 클래스
class UpbitSignal(QThread):
    # 시그널 함수 선언(정의)
    coinDataSent = pyqtSignal(float, float, float, float, float, float, float, float)

    def run(self):
        while(True): # 무한루프
            url = "https://api.upbit.com/v1/ticker"
            param = {"markets": "KRW-BTC"}
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

            self.coinDataSent.emit(
                float(trade_price), float(high_price),
                float(low_price), float(closing_price),
                float(trade_vol), float(trade_vol_24),
                float(trade_price_24), float(change_rate)
                 )
            # 업비트 api 호출 딜레이 3초
            time.sleep(3)

class MainWindow(QMainWindow, form_class):  # 슬롯 클래스
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # ui 불러오기
        self.setWindowTitle("비트코인 정보 프로그램 v0.5")

        self.ubs = UpbitSignal()  # 시그널 클래스로 객체 선언
        self.ubs.coinDataSent.connect(self.fillCoinData)
        self.ubs.start() # 시그널 클래스 run() 실행

    def fillCoinData(self, a,b,c,d,e,f,g,h):
        self.trade_price.setText(f"{a: ,.0f}")  # trade_price는 ui에 있는 레이블 이름
        self.high_price.setText(f"{b:,.0f}")
        self.low_price.setText(f"{c:,.0f}")
        self.closing_price.setText(f"{d:,.0f}")
        self.trade_vol.setText(f"{e:,.3f}")
        self.trade_vol_24.setText(f"{f:,.3f}")
        self.trade_price_24.setText(f"{g:,.0f}")
        self.change_rate.setText(f"{h:.2f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())