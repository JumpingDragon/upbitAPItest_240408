import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("ui/comboBoxtest.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.comboBox_setting()
        self.comboBox.currentIndexChanged.connect(self.menuSelected) # 이벤트 함수

    def comboBox_setting(self):  # 콤보박스 셋팅
        menulist = ['   ', 'Charlie Puth', '태연', '비비', '아이유', 'Taylor Swift', 'Selena Gomez']
        menulist = sorted(menulist)
        self.comboBox.addItems(menulist)

    def menuSelected(self):  # 콤보박스 메뉴가 변경되었을 때 호출되는 함수
        Label = self.comboBox.currentText()
        self.output_label.setText(Label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
