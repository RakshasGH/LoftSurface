# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from View.Plot.Plot2DWithInfo import Plot2DWithInfo


class PlotSettings:
    def __init__(self, controller):
        self.controller = controller
        self.mainLayout = QtWidgets.QVBoxLayout()

        # сведения о положении мыши относительно СК графика
        self.lblPos = QtWidgets.QLabel()
        self.lblPos.setFixedWidth(150)
        self.lblPos.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)

        # фрейм для отрисовки графиков
        self.frameCanvas = Plot2DWithInfo(self.lblPos)

        # разрешение на отрисовку кривой из двух конических сечений
        self.cbDrawBezier = QtWidgets.QCheckBox("Кривые Безье")
        self.cbDrawBezier.setChecked(True)
        self.cbDrawBezier.clicked.connect(self.controller.on_clicked_cbDrawBezier)

        # разрешение на отрисовку периодического B-сплайна
        self.cbDrawBSpline = QtWidgets.QCheckBox("B-сплайн")
        self.cbDrawBSpline.setChecked(True)
        self.cbDrawBSpline.clicked.connect(self.controller.on_clicked_cbDrawBSpline)

        # кнопка для очистки содержимого канвы
        self.btnClearCanvas = QtWidgets.QPushButton("Очистить")
        self.btnClearCanvas.clicked.connect(self.controller.on_clicked_btnClearCanvas)

        # размещение виджетов

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.cbDrawBezier)
        hbox.addWidget(self.cbDrawBSpline)
        hbox.addWidget(self.btnClearCanvas, stretch=0)
        hbox.addWidget(self.lblPos, alignment=QtCore.Qt.AlignRight, stretch=1)

        self.mainLayout.addWidget(self.frameCanvas, stretch=1)
        self.mainLayout.addLayout(hbox, stretch=0)
