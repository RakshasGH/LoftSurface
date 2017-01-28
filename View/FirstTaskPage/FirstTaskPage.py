# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
import numpy as np

from View.FirstTaskPage.PlotSettings import PlotSettings
from View.FirstTaskPage.FreemanSettings import FreemanSettings
from Model.Freeman import Freeman


class FirstTaskPage(QtWidgets.QFrame):
    def __init__(self, stack):
        QtWidgets.QFrame.__init__(self)
        self.stack = stack

        self.model = None  # заданная кодом Фримена фигура
        self.step = "InvMove"  # для пошагового режима

        # используемые виджеты
        self.plotSettings = PlotSettings()
        self.freemanSettings = FreemanSettings(self)

        # кнопка для возврата в главное меню
        self.btnHome = QtWidgets.QPushButton("На стартовую страницу")
        self.btnHome.clicked.connect(self.on_clicked_btnHome)

        # размещение виджетов

        hbox = QtWidgets.QHBoxLayout()

        hbox.addLayout(self.freemanSettings.mainLayout, stretch=0)
        hbox.addLayout(self.plotSettings.mainLayout, stretch=1)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.btnHome)

        self.setLayout(vbox)

    # ==========================================================
    # переход на главную страницу
    # ==========================================================
    def on_clicked_btnHome(self):
        self.stack.setCurrentIndex(0)

    # ==========================================================
    # отрисовка фигуры заданной кодом Фримена
    # ==========================================================
    def on_clicked_btnDrawFreeman(self):
        self.plotSettings.frameCanvas.resetDictDraw()

        xStart, yStart = 3, 3
        code = self.freemanSettings.edtFreeman.text()

        self.model = Freeman(xStart, yStart, code)
        if self.model.abc is not None:
            self.plotSettings.frameCanvas.draw(self.model.abc.tolist(), "Freeman", QtCore.Qt.red)
        else:
            self.model = None

    # ==========================================================
    # выполнение отрицательного поворота
    # ==========================================================
    def on_clicked_btnNegRotate(self):
        if self.model is not None:
            self.plotSettings.frameCanvas.resetDictDraw()

            mm = Freeman()
            mm.abc = self.model.abc
            mm.abc = mm.NegRotate(int(self.freemanSettings.edtNegRotate.text()))

            self.plotSettings.frameCanvas.draw(mm.abc.tolist(), "NegRotate", QtCore.Qt.magenta)

    # ==========================================================
    # выполнение перемещения
    # ==========================================================
    def on_clicked_btnMove(self):
        if self.model is not None:
            self.plotSettings.frameCanvas.resetDictDraw()

            mm = Freeman()
            mm.abc = self.model.abc
            mm.abc = mm.NegRotate(int(self.freemanSettings.edtNegRotate.text()))
            mm.abc = mm.Move(int(self.freemanSettings.edtMove.text()))

            self.plotSettings.frameCanvas.draw(mm.abc.tolist(), "Move", QtCore.Qt.darkCyan)

    # ==========================================================
    # выполнение масштабирования
    # ==========================================================
    def on_clicked_Scaling(self):
        if self.model is not None:
            self.plotSettings.frameCanvas.resetDictDraw()

            mm = Freeman()
            mm.abc = self.model.abc
            mm.abc = mm.NegRotate(int(self.freemanSettings.edtNegRotate.text()))
            mm.abc = mm.Move(int(self.freemanSettings.edtMove.text()))
            mm.abc = mm.Scaling(float(self.freemanSettings.edtScalingX.text()), float(self.freemanSettings.edtScalingY.text()))

            self.plotSettings.frameCanvas.draw(mm.abc.tolist(), "Scaling", QtCore.Qt.darkYellow)

    # ==========================================================
    # установка пошагового режима
    # ==========================================================
    def on_clicked_check(self):
        if self.freemanSettings.cbMirror.isChecked():
            self.step = "Original"
            self.freemanSettings.btnMirror.setText("Показать исходные данные")
        else:
            self.step = "InvMove"
            self.freemanSettings.btnMirror.setText("Отразить")

    # ==========================================================
    # выполнение отражения
    # ==========================================================
    def on_clicked_Mirror(self):
        if self.model is not None:
            self.plotSettings.frameCanvas.resetDictDraw()

            mm = Freeman()
            mm.abc = self.model.abc
            mm.abc = mm.NegRotate(int(self.freemanSettings.edtNegRotate.text()))
            mm.abc = mm.Move(int(self.freemanSettings.edtMove.text()))
            mm.abc = mm.Scaling(float(self.freemanSettings.edtScalingX.text()), float(self.freemanSettings.edtScalingY.text()))

            DIVISIONS = self.plotSettings.frameCanvas.divisions

            # прямая и треугольник смещенные вниз по y
            pt = np.matrix([[-DIVISIONS, mm.func_line(-DIVISIONS), 0, 1],
                            [DIVISIONS,  mm.func_line(DIVISIONS),  0, 1]])

            line = Freeman()
            line.abc = pt

            if self.step == "Original":
                res = line.abc
                self.plotSettings.frameCanvas.draw(res.tolist(), "Line Original", QtCore.Qt.blue)

                res = mm.abc
                self.plotSettings.frameCanvas.draw(res.tolist(), "Original", QtCore.Qt.blue)

            if self.step == "Move":
                res = line.Mirror(0)
                self.plotSettings.frameCanvas.draw(res.tolist(), "Line Mirror 0", QtCore.Qt.blue)

                res = mm.Mirror(0)
                self.plotSettings.frameCanvas.draw(res.tolist(), "Mirror 0", QtCore.Qt.blue)

            if self.step == "Rotate":
                res = line.Mirror(1)
                self.plotSettings.frameCanvas.draw(res.tolist(), "Line Mirror 1", QtCore.Qt.blue)

                res = mm.Mirror(1)
                self.plotSettings.frameCanvas.draw(res.tolist(), "Mirror 1", QtCore.Qt.blue)

            if self.step == "Mirror":
                res = line.Mirror(2)
                self.plotSettings.frameCanvas.draw(res.tolist(), "Line Mirror 2", QtCore.Qt.blue)

                res = mm.Mirror(2)
                self.plotSettings.frameCanvas.draw(res.tolist(), "Mirror 2", QtCore.Qt.blue)

            # обратно

            if self.step == "InvRotate":
                res = line.Mirror(3)
                self.plotSettings.frameCanvas.draw(res.tolist(), "Line Mirror 3", QtCore.Qt.blue)

                res = mm.Mirror(3)
                self.plotSettings.frameCanvas.draw(res.tolist(), "Mirror 3", QtCore.Qt.blue)

            if self.step == "InvMove":
                res = line.Mirror()
                self.plotSettings.frameCanvas.draw(res.tolist(), "Line Mirror", QtCore.Qt.blue)

                res = mm.Mirror()
                self.plotSettings.frameCanvas.draw(res.tolist(), "Mirror", QtCore.Qt.blue)

            if self.freemanSettings.cbMirror.isChecked():
                if self.step == "Original":
                    self.step = "Move"
                    self.freemanSettings.btnMirror.setText("Выполнить перенос (1 шаг)")
                elif self.step == "Move":
                    self.step = "Rotate"
                    self.freemanSettings.btnMirror.setText("Выполнить поворот (2 шаг)")
                elif self.step == "Rotate":
                    self.step = "Mirror"
                    self.freemanSettings.btnMirror.setText("Выполнить отражение (3 шаг)")
                elif self.step == "Mirror":
                    self.step = "InvRotate"
                    self.freemanSettings.btnMirror.setText("Выполнить обратный поворот (4 шаг)")
                elif self.step == "InvRotate":
                    self.step = "InvMove"
                    self.freemanSettings.btnMirror.setText("Выполнить обратный перенос (5 шаг)")
                else:
                    self.step = "Original"
                    self.freemanSettings.btnMirror.setText("Показать исходные данные")
            else:
                self.step = "InvMove"
                self.freemanSettings.btnMirror.setText("Отразить")

    # ==========================================================
    # выполнение комплексного преобразования
    # ==========================================================
    def on_clicked_Complex(self):
        if self.model is not None:
            self.plotSettings.frameCanvas.resetDictDraw()

            mm = Freeman()
            mm.abc = self.model.abc
            mm.abc = mm.NegRotate(int(self.freemanSettings.edtNegRotate.text()))
            mm.abc = mm.Move(int(self.freemanSettings.edtMove.text()))
            mm.abc = mm.Scaling(float(self.freemanSettings.edtScalingX.text()), float(self.freemanSettings.edtScalingY.text()))
            mm.abc = mm.Mirror()

            self.plotSettings.frameCanvas.draw(mm.abc.tolist(), "Complex", QtCore.Qt.green)
