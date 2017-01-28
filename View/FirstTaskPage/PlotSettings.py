# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from View.Plot.Plot2DWithInfo import Plot2DWithInfo


class PlotSettings:
    def __init__(self):
        self.mainLayout = QtWidgets.QVBoxLayout()

        # сведения о положении мыши относительно СК графика
        self.lblPos = QtWidgets.QLabel()
        self.lblPos.setFixedWidth(150)
        self.lblPos.setAlignment(QtCore.Qt.AlignRight)

        # фрейм для отрисовки графиков
        self.frameCanvas = Plot2DWithInfo(self.lblPos)

        # размещение виджетов

        self.mainLayout.addWidget(self.frameCanvas, stretch=1)
        self.mainLayout.addWidget(self.lblPos, stretch=0, alignment=QtCore.Qt.AlignRight)
