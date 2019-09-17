import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication


if __name__ == '__main__':

    app = QApplication(sys.argv)

    # 创建窗口对象
    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    # 窗口标题
    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())