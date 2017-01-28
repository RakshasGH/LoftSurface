# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets, QtGui
from View.MainPage import MainPage


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.widget = MainPage()
        self.setCentralWidget(self.widget)

        # меню
        self.myMenuBar = QtWidgets.QMenuBar()
        self.setMenuBar(self.myMenuBar)
        self.menuFile = QtWidgets.QMenu("&Файл")
        self.actClose = QtWidgets.QAction("Выход", None)
        self.actClose.setShortcut(QtGui.QKeySequence.Close)
        self.actClose.triggered.connect(self.on_close)
        self.menuFile.addAction(self.actClose)
        self.actMenuFile = self.myMenuBar.addMenu(self.menuFile)
        self.menuHelp = self.myMenuBar.addMenu("&Справка")
        self.actHelp = QtWidgets.QAction("Техническое задание", None)
        self.actHelp.setShortcut("F1")
        self.actHelp.triggered.connect(self.on_help)
        self.menuHelp.addAction(self.actHelp)

    # ==========================================================
    # закрытие окна
    # ==========================================================
    def on_close(self):
        sys.exit()

    # ==========================================================
    # вызов справки
    # ==========================================================
    def on_help(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    mainWindow = MyWindow()
    mainWindow.setWindowTitle("Курсовой проект by Мян Р.А.")
    mainWindow.show()

    sys.exit(app.exec_())
