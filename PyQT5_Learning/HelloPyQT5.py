"""参考自https://maicss.gitbooks.io/pyqt5/content/hello_world.html"""
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QToolTip, QPushButton, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication


class QTExample(QWidget):
    def __init__(self):
        # super()构造器方法返回父级的对象。__init__()方法是构造器的一个方法。
        super().__init__()
        # 使用initUI()方法创建一个GUI
        self.initUI()

    def initUI(self):
        # ExampleCenter
        self.resize(450, 250)
        # 调用我们下面写的，实现对话框居中的方法。
        self.center()
        self.setWindowTitle('Hello PyQT5')

        # ExampleQIcon
        # 自己需要准备一个web.png
        # setGeometry()有两个作用：把窗口放到屏幕上并且设置窗口大小。参数分别代表屏幕坐标的x、y和窗口大小的宽、高。这个方法是resize()和move()的合体。
        # self.setGeometry(300, 300, 300, 220)
        self.setWindowIcon(QIcon('robot.png'))

        # Example_setFont
        # 设置了提示框的字体，我们使用了10px的SansSerif字体
        QToolTip.setFont(QFont('SansSerif', 10))
        # 调用setTooltip()创建提示框可以使用富文本格式的内容。
        self.setToolTip('This is a <b>QWidget</b> widget')
        # 创建一个按钮，并且为按钮添加了一个提示框。
        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        # # 调整按钮大小，并让按钮在屏幕上显示出来，sizeHint()方法提供了一个默认的按钮大小。
        btn.resize(btn.sizeHint())
        btn.move(170, 60)

        # ExampleQuit
        # 创建一个继承自QPushButton的按钮
        qbtn = QPushButton('Quit', self)
        # 点击按钮之后，信号会被捕捉并给出既定的反应。
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(170, 120)

        self.show()

    def center(self):
        # 获得主窗口所在的框架。
        qr = self.frameGeometry()
        # QtGui.QDesktopWidget提供了用户的桌面信息，包括屏幕的大小。
        # 获取显示器的分辨率，然后得到屏幕中间点的位置。
        cp = QDesktopWidget().availableGeometry().center()
        # 把主窗口框架的中心点放置到屏幕的中心位置。
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # ExampleMessageBox
    def closeEvent(self, event):
        # 如果关闭QWidget，就会产生一个QCloseEvent，并且把它传入到closeEvent函数的event参数中。改变控件的默认行为，就是替换掉默认的事件处理。
        # 最后一个参数是默认按钮，这个按钮是默认选中的。
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QTExample()
    # 创建窗口对象
    # QWidge控件是一个用户界面的基本控件，它提供了基本的应用构造器
    # w = QWidget()
    # resize()方法能改变控件的大小，这里的意思是窗口宽250px，高150px。
    # w.resize(250, 150)
    # move()是修改控件位置的的方法。它把控件放置到屏幕坐标的(300, 300)的位置（屏幕坐标系的原点是屏幕的左上角）
    # w.move(300, 300)
    # 窗口标题
    # ex.self.setWindowTitle('Simple')
    # 控件在内存里创建，使用show（）之后才能在显示器上显示出来。
    # w.show()

    sys.exit(app.exec_())
