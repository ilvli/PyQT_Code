import sys
from PyQt5.QtWidgets import (QApplication, QComboBox, QSpinBox, QLabel,
                           QDialog, QGridLayout, QDoubleSpinBox)
import urllib.request

# 注意
# 本例书中所给链接失效了,所以这个程序不能正常运行.

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        date = self.getdata()
        # 根据键进行重排序
        rates = sorted(self.rates.keys())

        dateLabel = QLabel(date)
        # QComboBox():组合框
        self.fromComboBox = QComboBox()
        self.fromComboBox.addItems(rates)
        # QDoubleSpinBox():可以处理浮点数据的微调框
        self.fromSpinBox = QDoubleSpinBox()
        # 在设置微调框的值之前先设置其取值范围
        self.fromSpinBox.setRange(0.01, 10000000.00)
        # 设置微调框的值
        self.fromSpinBox.setValue(1.00)
        self.toComboBox = QComboBox()
        self.toComboBox.addItems(rates)
        self.toLabel = QLabel("1.00")
        # 使用网格布局
        grid = QGridLayout()
        grid.addWidget(dateLabel, 0, 0)
        grid.addWidget(self.fromComboBox, 1, 0)
        grid.addWidget(self.fromSpinBox, 1, 1)
        grid.addWidget(self.toComboBox, 2, 0)
        grid.addWidget(self.toLabel, 2, 1)
        self.setLayout(grid)
        self.fromComboBox.currentIndexChanged.connect(self.updateUi)
        self.toComboBox.currentIndexChanged.connect(self.updateUi)
        self.fromSpinBox.valueChanged.connect(self.updateUi)
        self.setWindowTitle("Currency")

    def updateUi(self):
        to = str(self.toComboBox.currentText())
        from_ = str(self.fromComboBox.currentText())
        amount = ((self.rates[from_] / self.rates[to]) *
                  self.fromSpinBox.value())
        self.toLabel.setText("{0:.2f}".format(amount))

    # 下载数据并保存到字典里,返回一个数据所使用日期的字符串
    def getdata(self):
        # 字典key为币种,value为货币转换系数
        self.rates = {}
        try:
            data = "Unknown"
            data = urllib.request.urlopen(
                "http://www.bankofcanada.ca"
                "/en/markets/csv/exchange_eng.csv").read()
            for line in data.decode("utf8", "replace").split("\n"):
                line = line.rstrip()
                if not line or line.startswith(("#", "Closing")):
                    continue
                fields = line.split(",")
                if line.startswith("Date "):
                    date = fields[-1]
                else:
                    try:
                        value = float(fields[-1])
                        self.rates[str(fields[0])] = value
                    except ValueError:
                        pass
            return "Exchange Rates Date: " + date
        except Exception as e:
            return "Failed to download:\n{0}".format(e)

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()