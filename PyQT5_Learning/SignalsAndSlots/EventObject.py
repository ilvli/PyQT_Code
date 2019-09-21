"""
事件对象是用python来描述一系列的事件自身属性的对象。
在本例中我们用标签来显示鼠标的坐标
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建布局
        grid = QGridLayout()
        # ？？？
        grid.setSpacing(10)

        x = 0
        y = 0

        # 在Qlabel组件里显示鼠标的X和Y坐标。
        self.text = "x: {0},  y: {1}".format(x, y)
        self.label = QLabel(self.text, self)

        # 添加组件
        grid.addWidget(self.label, 0, 0, Qt.AlignTop)

        # 追踪鼠标事件
        self.setMouseTracking(True)

        self.setLayout(grid)
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Event object')
        self.show()

    # 事件追踪默认没有开启，当开启后才会追踪鼠标的点击事件。
    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()

        text = "x: {0},  y: {1}".format(x, y)
        self.label.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
