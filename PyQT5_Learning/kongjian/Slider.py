"""
This example shows a QSlider widget.
"""

from PyQt5.QtWidgets import (QWidget, QSlider, QLabel, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个水平的`QSlider`。
        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(30, 40, 100, 30)
        # 把`valueChanged`信号跟`changeValue()`方法关联起来。
        sld.valueChanged[int].connect(self.changeValue)

        # 创建一个`QLabel`组件并给它设置一个静音图标。
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('../open.png'))
        self.label.setGeometry(160, 40, 80, 30)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QSlider')
        self.show()

    def changeValue(self, value):
        # 根据音量值的大小更换标签位置的图片。这段代码是：如果音量为0，就把图片换成mute.png。
        if value == 0:
            self.label.setPixmap(QPixmap('../poison.png'))
        elif value > 0 and value <= 30:
            self.label.setPixmap(QPixmap('../quit.png'))
        elif value > 30 and value < 80:
            self.label.setPixmap(QPixmap('../robot.png'))
        else:
            self.label.setPixmap(QPixmap('../open.png'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
