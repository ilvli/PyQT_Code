"""
参考自https://maicss.gitbooks.io/pyqt5/content/hello_world.html
PyQT5关于布局的代码演示
"""
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QHBoxLayout, QVBoxLayout


# 在PyQT5中有有两种方式可以搞定布局：绝对定位和PyQt5的layout类
class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 下面是绝对布局的演示，我们使用move()方法定位了每一个元素，使用x、y坐标。x、y坐标的原点是程序的左上角。
        lbl1 = QLabel('Zetcode', self)
        lbl1.move(15, 10)
        lbl2 = QLabel('tutorials', self)
        lbl2.move(35, 40)
        lbl3 = QLabel('for programmers', self)
        lbl3.move(55, 70)

        self.setGeometry(600, 400, 350, 250)
        self.setWindowTitle('布局')
        self.show()


# 使用盒布局能让程序具有更强的适应性
# QHBoxLayout`和`QVBoxLayout`是基本的布局类，分别是水平布局和垂直布局。
class Example2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 在应用的右下角放了两个按钮
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        # 创建一个水平布局，增加两个按钮和弹性空间。stretch函数在两个按钮前面增加了一些弹性空间
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        # 将水平布局放在QVBoxLayout垂直布局盒之中，stretch函数在两个按钮上面增加了一些弹性空间
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        # 使布局可见
        self.setLayout(vbox)

        self.setGeometry(600, 400, 350, 250)
        self.setWindowTitle('Buttons')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example2()
    sys.exit(app.exec_())
