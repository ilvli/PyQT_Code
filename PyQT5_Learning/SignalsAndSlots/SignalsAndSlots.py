"""
调用应用的exec_()方法时，应用会进入主循环，主循环会监听和分发事件。

在事件模型中，有三个角色：
    事件源: 发生了状态改变的对象。
    事件: 这个对象状态改变的内容。
    事件目标: 事件想作用的目标。
事件源绑定事件处理函数，然后作用于事件目标身上。

PyQt5处理事件方面有个signal and slot机制。Signals and slots用于对象间的通讯。事件触发的时候，发生一个signal，slot是
用来被Python调用的（相当于一个句柄？这个词也好恶心，就是相当于事件的绑定函数）slot只有在事件触发的时候才能调用。

`sender`是信号的发送者，`receiver`是信号的接收者，`slot`是对这个信号应该做出的反应。
"""
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider, QVBoxLayout, QApplication)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # LCD数字显示器（我自己想的名称）
        lcd = QLCDNumber(self)
        # 滑条
        sld = QSlider(Qt.Horizontal, self)

        # 是垂直布局器
        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)
        self.setLayout(vbox)

        # 把滑块的变化和数字的变化绑定在一起。
        sld.valueChanged.connect(lcd.display)

        self.setGeometry(300, 300, 350, 150)
        self.setWindowTitle('Signal and slot')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
