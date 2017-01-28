# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from View.FirstTaskPage.FirstTaskPage import FirstTaskPage
from View.SecondTaskPage.SecondTaskPage import SecondTaskPage
from View.ThirdTaskPage.ThirdTaskPage import ThirdTaskPage


class MainPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.lblTitle = QtWidgets.QLabel(
            '<center><font size="10" color="black">' +
            'Курсовой проект по курсам<br>' +
            '<b>Графические системы</b><br>' +
            'и<br>' +
            '<b>Геометрическое моделирование в САПР</b>' +
            '</font></center>')

        # кнопки для переходов к реализациям заданий курсового проекта
        self.btnTaskOne = QtWidgets.QPushButton("Практическое задание №1\n"
                                                "Двумерные модели и аффинные преобразования")
        self.btnTaskOne.clicked.connect(self.on_clicked_btnTaskOne)
        self.btnTaskTwo = QtWidgets.QPushButton("Практическое задание №2\n"
                                                "Аппроксимирующие кривые")
        self.btnTaskTwo.clicked.connect(self.on_clicked_btnTaskTwo)
        self.btnTaskThree = QtWidgets.QPushButton("Практическое задание №3\n"
                                                  "Lofting поверхности")
        self.btnTaskThree.clicked.connect(self.on_clicked_btnTaskThree)

        # главная страница
        self.frameMainPage = QtWidgets.QFrame()

        # контейнер со страницами
        self.stack = QtWidgets.QStackedLayout()

        # страница для задачи 1
        self.frameTaskOne = FirstTaskPage(self.stack)

        # страница для задачи 2
        self.frameTaskTwo = SecondTaskPage(self.stack)

        # страница для задачи 3
        self.frameTaskThree = ThirdTaskPage(self.stack)

        # размещение виджетов

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.lblTitle)
        vbox.addWidget(self.btnTaskOne)
        vbox.addWidget(self.btnTaskTwo)
        vbox.addWidget(self.btnTaskThree)

        self.frameMainPage.setLayout(vbox)

        self.stack.addWidget(self.frameMainPage)
        self.stack.addWidget(self.frameTaskOne)
        self.stack.addWidget(self.frameTaskTwo)
        self.stack.addWidget(self.frameTaskThree)

        self.setLayout(self.stack)

    # ==========================================================
    # обработчик нажатия на кнопку "Практическое задание №1.."
    # ==========================================================
    def on_clicked_btnTaskOne(self):
        self.stack.setCurrentWidget(self.frameTaskOne)

    # ==========================================================
    # обработчик нажатия на кнопку "Практическое задание №2.."
    # ==========================================================
    def on_clicked_btnTaskTwo(self):
        self.stack.setCurrentWidget(self.frameTaskTwo)

    # ==========================================================
    # обработчик нажатия на кнопку "Практическое задание №3.."
    # ==========================================================
    def on_clicked_btnTaskThree(self):
        self.stack.setCurrentWidget(self.frameTaskThree)
