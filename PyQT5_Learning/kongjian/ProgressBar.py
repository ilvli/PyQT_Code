"""
This example shows a QProgressBar widget.
"""
from PyQt5.QtWidgets import (QWidget, QApplication, QProgressBar, QPushButton)
from PyQt5.QtCore import QBasicTimer
import sys


# `QProgressBar`组件提供了水平和垂直两种进度条，进度条可以设置最大值和最小值，默认情况是0~99。
class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个进度条
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.btn = QPushButton('Start', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.doAction)

        # 用时间控制进度条。
        self.timer = QBasicTimer()
        self.step = 0

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QProgressBar')
        self.show()

    # 每个`QObject`和又它继承而来的对象都有一个`timerEvent()`事件处理函数。为了触发事件，我们重载了这个方法
    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Finished')
            return

        # step值
        self.step = self.step + 1
        self.pbar.setValue(self.step)

    # 用来控制开始和停止的
    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            # 调用`start()`方法加载一个时间事件。这个方法有两个参数：过期时间和事件接收者。
            self.timer.start(100, self)
            self.btn.setText('Stop')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
