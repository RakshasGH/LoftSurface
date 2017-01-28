# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore

from View.Plot.Plot3D import Plot3D


class PlotSettings:
    def __init__(self, controller):
        self.controller = controller
        self.mainLayout = QtWidgets.QVBoxLayout()

        # фрейм для отрисовки графиков
        self.frameCanvas = Plot3D()

        # поля для задания угла поворота вокруг оси
        self.edtAngleX = QtWidgets.QDoubleSpinBox()
        self.edtAngleY = QtWidgets.QDoubleSpinBox()
        for edtAngle in self.edtAngleX, self.edtAngleY:
            edtAngle.setRange(-360.0, 360.0)
            edtAngle.setDecimals(5)
            edtAngle.setSingleStep(10.0)
            edtAngle.valueChanged[float].connect(self.controller.on_value_changed_Angle)
        self.edtAngleX.setValue(-35.26439)
        self.edtAngleY.setValue(45.0)

        # размещение виджетов

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel("Поворот вокруг оси X:"), alignment=QtCore.Qt.AlignRight, stretch=1)
        hbox.addWidget(self.edtAngleX)
        hbox.addWidget(QtWidgets.QLabel("Поворот вокруг оси Y:"))
        hbox.addWidget(self.edtAngleY)

        self.mainLayout.addWidget(self.frameCanvas, stretch=1)
        self.mainLayout.addLayout(hbox, stretch=0)
