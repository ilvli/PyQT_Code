from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
import sys, random


class Tetris(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建了一个Board类的实例，并设置为应用的中心组件。Board的定义在下面（设置中心组件有什么用？？？）
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)

        # 创建一个`statusbar`来显示三种信息：消除的行数，游戏暂停状态或者游戏结束状态。
        self.statusbar = self.statusBar()
        # `msg2Statusbar`是一个自定义的信号，用在（和）Board类（交互），`showMessage()`方法是一个内建的，用来在statusbar上显示信息的方法。
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        # 初始化游戏：
        self.tboard.start()

        self.resize(180, 380)
        self.center()
        self.setWindowTitle('Tetris')
        self.show()

    def center(self):
        '''centers the window on the screen'''
        screen = QDesktopWidget().screenGeometry()
        # size=(0, 0, 180, 380)
        size = self.geometry()
        # 将窗口移到中心位置
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


class Board(QFrame):
    # 创建了一个自定义信号`msg2Statusbar`，当我们想往`statusbar`里显示信息的时候，发出这个信号就行了。
    msg2Statusbar = pyqtSignal(str)
    # 这些是`Board`类的变量。`BoardWidth`和`BoardHeight`分别是board的宽度和高度。
    BoardWidth = 10
    BoardHeight = 22
    # `Speed`是游戏的速度，每300ms出现一个新的方块。
    Speed = 300

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        # 在`initBoard()`里初始化了一些重要的变量。`self.board`定义了方块的形状和位置，取值范围是0 - 7。
        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False

        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.board = []

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()

    # `shapeAt()`决定了board里方块的的种类。
    def shapeAt(self, x, y):
        return self.board[(y * Board.BoardWidth) + x]

    def setShapeAt(self, x, y, shape):
        '''sets a shape at the board'''
        self.board[(y * Board.BoardWidth) + x] = shape

    # board的大小可以动态的改变。所以方格的大小也应该随之变化。
    # `squareWidth()`计算并返回每个块应该占用多少像素 - -也即`Board.BoardWidth`。
    def squareWidth(self):
        return self.contentsRect().width() // Board.BoardWidth

    def squareHeight(self):
        return self.contentsRect().height() // Board.BoardHeight

    def start(self):
        '''starts game'''
        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clearBoard()

        self.msg2Statusbar.emit(str(self.numLinesRemoved))

        self.newPiece()
        self.timer.start(Board.Speed, self)

    # `pause()`方法用来暂停游戏，停止计时并在`statusbar`上显示一条信息。
    def pause(self):
        '''pauses game'''
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.msg2Statusbar.emit("paused")

        else:
            self.timer.start(Board.Speed, self)
            self.msg2Statusbar.emit(str(self.numLinesRemoved))

        self.update()

    # 渲染是在paintEvent()方法里发生的`QPainter`负责PyQt5里所有低级绘画操作。
    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()

        # 渲染游戏分为两步。第一步是先画出所有已经落在最下面的的图，这些保存在`self.board`里。可以使用`shapeAt()`查看这个这个变量。
        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.shapeAt(j, Board.BoardHeight - i - 1)
                if shape != Tetrominoe.NoShape:
                    self.drawSquare(painter,
                                    rect.left() + j * self.squareWidth(),
                                    boardTop + i * self.squareHeight(), shape)
        # 第二步是画出更在下落的方块。
        if self.curPiece.shape() != Tetrominoe.NoShape:
            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                                boardTop + (Board.BoardHeight - y - 1) * self.squareHeight(), self.curPiece.shape())

    def keyPressEvent(self, event):
        '''processes key press events'''
        if not self.isStarted or self.curPiece.shape() == Tetrominoe.NoShape:
            super(Board, self).keyPressEvent(event)
            return
        key = event.key()
        if key == Qt.Key_P:
            self.pause()
            return
        if self.isPaused:
            return
        elif key == Qt.Key_Left:
            self.tryMove(self.curPiece, self.curX - 1, self.curY)
        # 在`keyPressEvent()`方法获得用户按下的按键。如果按下的是右方向键，就尝试把方块向右移动，说尝试是因为有可能到边界不能移动了。
        elif key == Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)
        elif key == Qt.Key_Down:
            self.tryMove(self.curPiece.rotateRight(), self.curX, self.curY)
        # 上方向键是把方块向左旋转一下
        elif key == Qt.Key_Up:
            self.tryMove(self.curPiece.rotateLeft(), self.curX, self.curY)
        # 空格键会直接把方块放到底部
        elif key == Qt.Key_Space:
            self.dropDown()
        elif key == Qt.Key_D:
            self.oneLineDown()
        else:
            super(Board, self).keyPressEvent(event)

    # 在计时器事件里，要么是等一个方块下落完之后创建一个新的方块，要么是让一个方块直接落到底（move a falling piece one line down）。
    def timerEvent(self, event):
        '''handles timer event'''
        if event.timerId() == self.timer.timerId():
            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newPiece()
            else:
                self.oneLineDown()
        else:
            super(Board, self).timerEvent(event)

    # `clearBoard(`)方法通过`Tetrominoe.NoShape`清空`broad`。
    def clearBoard(self):
        '''clears shapes from the board'''
        for i in range(Board.BoardHeight * Board.BoardWidth):
            self.board.append(Tetrominoe.NoShape)

    def dropDown(self):
        '''drops down a shape'''
        newY = self.curY
        while newY > 0:
            if not self.tryMove(self.curPiece, self.curX, newY - 1):
                break
            newY -= 1

        self.pieceDropped()

    def oneLineDown(self):
        '''goes one line down with a shape'''
        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
            self.pieceDropped()

    def pieceDropped(self):
        '''after dropping shape, remove full lines and create new shape'''
        for i in range(4):
            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.removeFullLines()

        if not self.isWaitingAfterLine:
            self.newPiece()

    # 如果方块碰到了底部，就调用`removeFullLines()`方法，找到所有能消除的行消除它们。
    # 消除的具体动作就是把符合条件的行消除掉之后，再把它上面的行下降一行。
    # 注意移除满行的动作是倒着来的，因为我们是按照重力来表现游戏的，如果不这样就有可能出现有些方块浮在空中的现象。
    def removeFullLines(self):
        '''removes all full lines from the board'''
        numFullLines = 0
        rowsToRemove = []

        for i in range(Board.BoardHeight):
            n = 0
            for j in range(Board.BoardWidth):
                if not self.shapeAt(j, i) == Tetrominoe.NoShape:
                    n = n + 1

            if n == 10:
                rowsToRemove.append(i)

        rowsToRemove.reverse()

        for m in rowsToRemove:
            for k in range(m, Board.BoardHeight):
                for l in range(Board.BoardWidth):
                    self.setShapeAt(l, k, self.shapeAt(l, k + 1))

        numFullLines = numFullLines + len(rowsToRemove)

        if numFullLines > 0:
            self.numLinesRemoved = self.numLinesRemoved + numFullLines
            self.msg2Statusbar.emit(str(self.numLinesRemoved))

            self.isWaitingAfterLine = True
            self.curPiece.setShape(Tetrominoe.NoShape)
            self.update()

    # `newPiece()`方法是用来创建形状随机的方块。如果随机的方块不能正确的出现在预设的位置，游戏结束。
    def newPiece(self):
        '''creates a new shape'''
        self.curPiece = Shape()
        self.curPiece.setRandomShape()
        self.curX = Board.BoardWidth // 2 + 1
        self.curY = Board.BoardHeight - 1 + self.curPiece.minY()

        if not self.tryMove(self.curPiece, self.curX, self.curY):
            self.curPiece.setShape(Tetrominoe.NoShape)
            self.timer.stop()
            self.isStarted = False
            self.msg2Statusbar.emit("Game over")

    # `tryMove()`是尝试移动方块的方法。如果方块已经到达board的边缘或者遇到了其他方块，就返回False。否则就把方块下落到想要
    def tryMove(self, newPiece, newX, newY):
        '''tries to move a shape'''
        for i in range(4):
            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)

            if x < 0 or x >= Board.BoardWidth or y < 0 or y >= Board.BoardHeight:
                return False

            if self.shapeAt(x, y) != Tetrominoe.NoShape:
                return False

        self.curPiece = newPiece
        self.curX = newX
        self.curY = newY
        self.update()

        return True

    def drawSquare(self, painter, x, y, shape):
        '''draws a square of a shape'''
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC, 0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2, self.squareHeight() - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1,
                         y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)


# `Tetrominoe`类保存了所有方块的形状。我们还定义了一个`NoShape`的空形状。
class Tetrominoe(object):
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7


# Shape类保存类方块内部的信息。
class Shape(object):
    # coordsTable元组保存了所有的方块形状的组成。是一个构成方块的坐标模版。
    coordsTable = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, -1), (0, 0), (-1, 0), (-1, 1)),
        ((0, -1), (0, 0), (1, 0), (1, 1)),
        ((0, -1), (0, 0), (0, 1), (0, 2)),
        ((-1, 0), (0, 0), (1, 0), (0, 1)),
        ((0, 0), (1, 0), (0, 1), (1, 1)),
        ((-1, -1), (0, -1), (0, 0), (0, 1)),
        ((1, -1), (0, -1), (0, 0), (0, 1))
    )

    def __init__(self):
        self.coords = [[0, 0] for i in range(4)]
        self.pieceShape = Tetrominoe.NoShape
        self.setShape(Tetrominoe.NoShape)

    def shape(self):
        '''returns shape'''
        return self.pieceShape

    def setShape(self, shape):
        '''sets a shape'''
        table = Shape.coordsTable[shape]

        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape

    def setRandomShape(self):
        '''chooses a random shape'''
        self.setShape(random.randint(1, 7))

    def x(self, index):
        '''returns x coordinate'''
        return self.coords[index][0]

    def y(self, index):
        '''returns y coordinate'''
        return self.coords[index][1]

    def setX(self, index, x):
        '''sets x coordinate'''
        self.coords[index][0] = x

    def setY(self, index, y):
        '''sets y coordinate'''
        self.coords[index][1] = y

    def minX(self):
        '''returns min x value'''
        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])

        return m

    def maxX(self):
        '''returns max x value'''
        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])

        return m

    def minY(self):
        '''returns min y value'''
        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])

        return m

    def maxY(self):
        '''returns max y value'''
        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])

        return m

    # `rotateLeft()`方法向右旋转一个方块。正方形的方块就没必要旋转，就直接返回了。其他的是返回一个新的，能表示这个形状旋转了的坐标。
    def rotateLeft(self):
        '''rotates shape to the left'''
        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):
            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))

        return result

    def rotateRight(self):
        '''rotates shape to the right'''
        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):
            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))

        return result


if __name__ == '__main__':
    app = QApplication([])
    tetris = Tetris()
    sys.exit(app.exec_())
