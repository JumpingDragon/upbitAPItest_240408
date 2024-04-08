import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class SignalThread(QThread): # 시그널 파트
    signal1 = pyqtSignal()      # signal 함수
    signal2 = pyqtSignal(int, int)

    def run(self):
        self.signal1.emit()
        self.signal2.emit(1000, 2000)

class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        signalClass = SignalThread()

        signalClass.signal1.connect(self.signal1_print)
        # 시그널 함수와 슬롯 함수를 연결
        signalClass.signal2.connect(self.signal2_print)
        # 시그널 함수와 슬롯 함수를 연결
        signalClass.run()

    @pyqtSlot()
    def signal1_print(self):    # slot 함수
        print("signal1 제출됨(emit)")

    @pyqtSlot(int, int)
    def signal2_print(self, a, b):    # slot 함수
        print(f"signal2 제출됨(emit) -> {a}, {b}")
        # 실제 프로그램에서는 윈도우에 출렫하는 내용이 와야 함.

app = QApplication(sys.argv)
win = MainWin()
win.show()
sys.exit(app.exec_())

