import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp, QMenu, QTextEdit
from PyQt5.QtGui import QIcon


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 调用`QtGui.QMainWindow`类的`statusBar()`方法，创建状态栏。
        # 第一次调用创建一个状态栏，返回一个状态栏对象。(状态栏在最下方)
        # `showMessage()`方法在状态栏上显示一条信息。
        self.statusBar().showMessage('Ready')

        # QAction`是菜单栏、工具栏或者快捷键的动作的组合。
        # 前面两行，我们创建了一个图标、一个exit的标签和一个快捷键组合，都执行了一个动作。
        # 第三行，创建了一个状态栏，当鼠标悬停在菜单栏的时候，能显示当前状态。
        exitAct = QAction(QIcon('poison.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')

        # 当执行这个指定的动作时，就触发了一个事件。这个事件跟`QApplication的quit()`行为相关联，所以这个动作就能终止这个应用。
        exitAct.triggered.connect(qApp.quit)

        # menuBar()`创建菜单栏。
        # 这里创建了一个菜单栏，并在上面添加了一个file菜单，并关联了点击退出应用的事件。
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        # 使用`QMenu`创建一个新菜单。
        impMenu = QMenu('Import', self)
        # 使用`addAction`添加一个动作。
        impAct = QAction('Import mail', self)
        impMenu.addAction(impAct)
        fileMenu.addMenu(impMenu)

        newAct = QAction('New', self)
        fileMenu.addAction(newAct)

        # 设置工具栏
        # 这里使用了一个行为对象，这个对象绑定了一个标签，一个图标和一个快捷键。
        # 这些行为被触发的时候，会调用`QtGui.QMainWindow`的quit方法退出应用。
        exitAct = QAction(QIcon('quit.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAct)

        # 这里创建了一个文本编辑区域，并把它放在`QMainWindow`的中间区域。
        # 这个组件或占满所有剩余的区域。
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        # 下面这段代码创建了一个行为菜单。这个行为／动作能切换状态栏显示或者隐藏。
        self.statusbar = self.statusBar()
        viewMenu = menubar.addMenu('View')
        # 用`checkable`选项创建一个能选中的菜单。
        viewStatAct = QAction('View statusbar', self, checkable=True)
        viewStatAct.setStatusTip('View statusbar')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.toggleMenu)
        viewMenu.addAction(viewStatAct)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Submenu')
        self.show()

    # 默认设置为选中状态。
    def toggleMenu(self, state):
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()

    # 创建一个右键可显的菜单
    def contextMenuEvent(self, event):
        cmenu = QMenu(self)

        # 创建菜单项
        newAct = cmenu.addAction("New")
        opnAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")

        # 使用`exec_()`方法显示菜单。从鼠标右键事件对象中获得当前坐标。
        # `mapToGlobal()`方法把当前组件的相对坐标转换为窗口（window）的绝对坐标。
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
        # 如果右键菜单里触发了事件，也就触发了退出事件，执行关闭菜单行为。
        if action == quitAct:
            qApp.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
