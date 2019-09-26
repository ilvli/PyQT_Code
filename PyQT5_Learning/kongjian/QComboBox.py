from PyQt5.QtWidgets import (QWidget, QLabel, QComboBox, QApplication)
import sys


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lbl = QLabel("Ubuntu", self)
        self.lbl.move(50, 150)

        # 创建一个`QComboBox`组件和五个选项。
        combo = QComboBox(self)
        combo.addItem("Ubuntu")
        combo.addItem("Mandriva")
        combo.addItem("Fedora")
        combo.addItem("Arch")
        combo.addItem("Gentoo")
        combo.move(50, 50)
        # 在选中的条目上调用`onActivated()`方法。
        combo.activated[str].connect(self.onActivated)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QComboBox')
        self.show()

    def onActivated(self, text):
        # 在方法内部，设置标签内容为选定的字符串，然后设置自适应文本大小。
        self.lbl.setText(text)
        self.lbl.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
