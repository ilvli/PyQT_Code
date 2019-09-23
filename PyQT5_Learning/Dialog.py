"""
本文件展示了PyQt5中4种对话框(Dialog)的用法
参考自https://maicss.gitbooks.io/pyqt5/content/hello_world.html
"""
from PyQt5.QtWidgets import (QWidget, QPushButton, QFrame, QColorDialog, QLineEdit, QFontDialog, QInputDialog,
                             QApplication, QLabel, QFileDialog, QMessageBox, qApp)
from PyQt5.QtGui import QColor
import sys


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个按键，关联到showDialog函数
        self.btn = QPushButton('InputDialog', self)
        self.btn.move(85, 20)
        self.btn.clicked.connect(self.showDialog)
        # 输入文本框
        self.le = QLineEdit(self)
        self.le.move(50, 60)

        # 初始化`QtGui.QFrame`的背景颜色。
        col = QColor(0, 0, 0)
        # 创建按键并关联showDialog函数
        self.btn = QPushButton('ColorDialog', self)
        self.btn.move(360, 20)
        self.btn.clicked.connect(self.showColorDialog)
        # 创建一个显示颜色的框
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % col.name())
        self.frm.setGeometry(320, 60, 170, 100)

        btnFont = QPushButton('FontDialog', self)
        # 按键自适应大小
        # btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btnFont.move(85, 250)
        btnFont.clicked.connect(self.showFontDialog)
        # 创建标签用于显示展示的文本
        self.lbl = QLabel('Knowledge only matters', self)
        self.lbl.move(50, 300)

        btnFile = QPushButton("FileDialog", self)
        btnFile.move(360, 250)
        btnFile.clicked.connect(self.showFileDialog)

        btnQuit = QPushButton('退出', self)
        btnQuit.move(240, 330)
        btnQuit.clicked.connect(qApp.quit)

        self.setGeometry(300, 300, 550, 380)
        self.setWindowTitle('dialog')
        self.show()

    def showDialog(self):
        # 第一个参数是输入框的标题，第二个参数是输入框的占位符。对话框返回输入内容和一个布尔值，如果点击的是OK按钮，布尔值就返回True。
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')
        if ok:
            self.le.setText(str(text))

    def showColorDialog(self):
        # 弹出一个`QColorDialog`对话框。
        col = QColorDialog.getColor()
        if col.isValid():
            self.frm.setStyleSheet("QWidget { background-color: %s }" % col.name())

    # 创建了一个有一个按钮和一个标签的`QFontDialog`的对话框，我们可以使用这个功能修改字体样式。
    def showFontDialog(self):
        # 弹出一个字体选择对话框。`getFont()`方法返回一个字体名称和状态信息。状态信息有OK和其他两种。
        font, ok = QFontDialog.getFont()
        # 如果点击OK，将标签设置为选择的格式
        if ok:
            self.lbl.setFont(font)

    # 将打开一个文本文件并显示出来
    def showFileDialog(self):
        # 显示标准的“打开”对话框，并获取用户文件名，而不必真正打开任何文件，只是把打开文件名称返回程序。
        # `getOpenFileName()`方法的第一个参数是说明文字，第二个参数是默认打开的文件夹路径。默认情况下显示所有类型的文件。
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        # 如果点了取消，返回false，否则返回文件名
        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                data = f.read()
                QMessageBox.about(self, "文件内容", data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
