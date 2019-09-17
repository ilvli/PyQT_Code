import sys
import time

from PyQt5.QtCore import (Qt, QTime, QTimer)
# from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication, QLabel)

# 每个程序都要有QApplication类用于访问全局信息
app = QApplication(sys.argv)
# 测试闹钟时间
# 为了方便，这里与原代码不同，请注意
testTime = "12:11"

try:
    due = QTime.currentTime()
    message = "Alert!"

    if len(testTime) < 2:
        raise ValueError
    # 格式化时间
    hours, mins = testTime.split(":")
    due = QTime(int(hours), int(mins))
    if not due.isValid():
        raise ValueError
    if len(sys.argv) > 2:
        message = " ".join(sys.argv[2:])
# 当没有给全参数时抛出错误
except ValueError:
    message = "Usage: alert.pyw HH:MM [optional message]"

while QTime.currentTime() < due:
    # 用sleep代替pass，提高速度
    time.sleep(20)

# 显示闹钟
label = QLabel("<font color=red size=72><b>{0}</b></font>"
               .format(message))
# 设置为SplashScreen（闪屏）模式，这样不会有标题栏
label.setWindowFlags(Qt.SplashScreen)
label.show()
# singleShot单位是毫秒，第一个参数为时间，第二个参数为时间到期后需要执行的函数或方法
QTimer.singleShot(60000, app.quit)
app.exec_()
