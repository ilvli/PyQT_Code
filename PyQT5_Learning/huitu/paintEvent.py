"""
本例写了一些文本上下居中对齐的俄罗斯Cylliric语言的文字，随机的绘制了一些点，绘制了一些填充了颜色的矩形，
用QPen绘制了一些直线，用QBrush绘制了矩形，用QPainterPath绘制了一个曲线。
"""
import sys, random
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPainterPath
from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.text = "Лев Николаевич Толстой\nАнна Каренина"

        self.setGeometry(300, 300, 350, 570)
        self.setWindowTitle('Drawing text')
        self.show()

    # 在绘画事件内完成绘画动作。
    def paintEvent(self, e):
        # `QPainter`是低级的绘画类。所有的绘画动作都在这个类的`begin()`和`end()`方法之间完成
        qp = QPainter()
        qp.begin(self)
        # 下面动作都封装在`draw_____()`函数内部了。
        self.drawText(e, qp)
        self.drawPoints(qp)
        self.drawRectangles(qp)
        self.drawLines(qp)
        self.drawBrushes(qp)
        qp.setRenderHint(QPainter.Antialiasing)
        self.drawBezierCurve(qp)
        qp.end()

    def drawText(self, event, qp):
        # 为文字绘画定义了笔和字体。
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10))
        # `drawText()`方法在窗口里绘制文本，`rect()`方法返回要更新的矩形区域。
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)

    def drawPoints(self, qp):
        qp.setPen(Qt.red)
        # 每次更改窗口大小，都会产生绘画事件，从`size()`方法里获得当前窗口的大小，然后把产生的点随机的分配到窗口的所有位置上。
        size = self.size()

        for i in range(1000):
            x = random.randint(1, size.width() - 1)
            y = random.randint(1, size.height() - 1)
            qp.drawPoint(x, y)

    # 使用QPen绘制矩形
    def drawRectangles(self, qp):
        # 使用16进制的方式定义一个颜色。
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)

        # 定义了一个笔刷，并画出了一个矩形。笔刷是用来画一个物体的背景。
        # `drawRect()`有四个参数，分别是矩形的x、y、w、h。 然后用笔刷和矩形进行绘画。
        qp.setBrush(QColor(200, 0, 0))
        qp.drawRect(10, 15, 90, 60)

        qp.setBrush(QColor(255, 80, 0, 160))
        qp.drawRect(130, 15, 90, 60)

        qp.setBrush(QColor(25, 0, 90, 200))
        qp.drawRect(250, 15, 90, 60)

    # 绘制直线
    def drawLines(self, qp):
        # 新建一个`QPen`对象，设置颜色黑色，宽2像素，这样就能看出来各个笔样式的区别。`Qt.SolidLine`是预定义样式的一种。
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        # 绘制直线，前两个参数为左端点的坐标，后两个参数为右端点的坐标
        qp.drawLine(50, 100, 280, 100)

        pen.setStyle(Qt.DashLine)
        qp.setPen(pen)
        qp.drawLine(50, 140, 280, 140)

        pen.setStyle(Qt.DashDotLine)
        qp.setPen(pen)
        qp.drawLine(50, 180, 280, 180)

        pen.setStyle(Qt.DotLine)
        qp.setPen(pen)
        qp.drawLine(50, 220, 280, 220)

        pen.setStyle(Qt.DashDotDotLine)
        qp.setPen(pen)
        qp.drawLine(50, 260, 280, 260)

        # 这里我们自定义了一个笔的样式。定义为`Qt.CustomDashLine`然后调用`setDashPattern()`方法。
        # 数字列表是线的样式，要求必须是个数为奇数，奇数位定义的是空格，偶数位为线长，数字越大，空格或线长越大
        # 比如本例的就是1像素线，4像素空格，5像素线，4像素空格。
        pen.setStyle(Qt.CustomDashLine)
        pen.setDashPattern([1, 4, 5, 4])
        qp.setPen(pen)
        qp.drawLine(50, 300, 280, 300)

    # 使用QBrush绘制矩形
    def drawBrushes(self, qp):
        # 创建了一个笔刷对象，添加笔刷样式，然后调用`drawRect()`方法画图。
        brush = QBrush(Qt.SolidPattern)
        qp.setBrush(brush)
        # drawRect的参数分别是：前两个参数是左上角端点的位置，后两个是长和宽
        qp.drawRect(10, 325, 90, 60)

        brush.setStyle(Qt.Dense1Pattern)
        qp.setBrush(brush)
        qp.drawRect(130, 325, 90, 60)

        brush.setStyle(Qt.Dense2Pattern)
        qp.setBrush(brush)
        qp.drawRect(250, 325, 90, 60)

        brush.setStyle(Qt.DiagCrossPattern)
        qp.setBrush(brush)
        qp.drawRect(10, 405, 90, 60)

        brush.setStyle(Qt.Dense5Pattern)
        qp.setBrush(brush)
        qp.drawRect(130, 405, 90, 60)

        brush.setStyle(Qt.Dense6Pattern)
        qp.setBrush(brush)
        qp.drawRect(250, 405, 90, 60)

        brush.setStyle(Qt.HorPattern)
        qp.setBrush(brush)
        qp.drawRect(10, 485, 90, 60)

        brush.setStyle(Qt.VerPattern)
        qp.setBrush(brush)
        qp.drawRect(130, 485, 90, 60)

        brush.setStyle(Qt.BDiagPattern)
        qp.setBrush(brush)
        qp.drawRect(250, 485, 90, 60)

    # 绘制贝塞尔曲线
    def drawBezierCurve(self, qp):
        # 用`QPainterPath`路径创建贝塞尔曲线。
        # 使用`cubicTo()`方法生成，分别需要三个点：起始点，控制点和终止点。
        path = QPainterPath()
        path.moveTo(20, 120)
        path.cubicTo(20, 120, 170, 400, 330, 120)

        # `drawPath()`绘制最后的图像。
        qp.drawPath(path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
