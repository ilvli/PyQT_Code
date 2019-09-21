"""
QObject`实例能发送事件信号。下面的例子是发送自定义的信号。
我们创建了一个叫closeApp的信号，这个信号会在鼠标按下的时候触发，事件与`QMainWindow`绑定。
"""

import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication


# `Communicate`类创建了一个`pyqtSignal()`属性的信号。
class Communicate(QObject):
    closeApp = pyqtSignal()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 点击窗口，即触发mousePressEvent时，发送closeApp信号，程序终止。
        self.c = Communicate()
        self.c.closeApp.connect(self.close)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Emit signal')
        self.show()

    # 点击窗口的时候，发送closeApp信号，程序终止。
    def mousePressEvent(self, event):
        self.c.closeApp.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())