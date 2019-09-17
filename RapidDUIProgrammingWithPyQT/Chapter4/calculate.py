from math import *
import sys
from PyQt5.QtWidgets import (QApplication, QTextBrowser,
                             QLineEdit, QVBoxLayout, QDialog)


# 表单的类
# 继承QDialog得到空白表单
class Form(QDialog):
    # 表单类的构造函数
    def __init__(self, parent=None):
        # 用super方法进行初始化
        super(Form, self).__init__(parent)
        # QTextBrowser()为只读文本框，不能对内容进行操作
        self.browser = QTextBrowser()
        # QLineEdit（）单行文本框。可给定初始化文本
        self.lineedit = QLineEdit("Type an expression and <Enter>")
        # 并将文本全部选中
        self.lineedit.selectAll()
        # 调整布局
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.lineedit)
        # 使布局管理器获得表单部件和该表单的所有权
        self.setLayout(layout)
        # 确定光标起始位置
        self.lineedit.setFocus()
        # returnPressed:当用户在文本框内输入回车键的时候发送信号
        # connect():当特定对象发射特定信号时调用指定函数
        self.lineedit.returnPressed.connect(self.updateUi)
        self.setWindowTitle("Calculate")

    def updateUi(self):
        try:
            text = self.lineedit.text()
            self.browser.append("{0} = <b>{1}</b>".format(text, eval(text)))
        except:
            # 如果错误就将错误输出到QTextBrowser
            self.browser.append(
                "<font color=red>{0} is invalid!</font>".format(text))


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
