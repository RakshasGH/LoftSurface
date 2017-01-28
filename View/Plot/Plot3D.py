# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui
import numpy as np

from View.Plot.PlotKernel import PlotKernel
from Model.Line import Line

AXIS_SIZE = 3


class Plot3D(PlotKernel):
    """
    Класс Plot3D реализует функционал для
    визуализации трехмерных графиков на экране
    """
    def __init__(self):
        PlotKernel.__init__(self)

    def paintEvent(self, e):
        canvas = QtGui.QPainter(self)
        # canvas.setRenderHint(QtGui.QPainter.Antialiasing)
        canvas.translate(self.axis_x, self.axis_y)

        # отрисовываем активные элементы
        for figure in self.dictDraw.items():
            if figure[1][2]:  # bVisible
                canvas.setPen(figure[1][1])  # pen
                canvas.drawPolyline(figure[1][0])  # pixels

    # ==========================================================
    # построить график по заданным точкам
    # ==========================================================
    def draw(self, coord, alias, color=QtCore.Qt.black, angleX=45, angleY=-35.26439):
        theta = -np.deg2rad(angleX)
        phi = -np.deg2rad(angleY)

        T = np.matrix([[np.cos(phi), np.sin(phi) * np.sin(theta),  0, 0],
                       [0,           np.cos(theta),                0, 0],
                       [np.sin(phi), -np.cos(phi) * np.sin(theta), 0, 0],
                       [0,           0,                            0, 1]])

        # ось 0X
        axisX = np.array([[0, 0, 0, 1], [self.divisions, 0, 0, 1]])
        pts = np.array(Line(axisX).build()).dot(T)
        self.addItem(pts.tolist(), "X", QtCore.Qt.red, AXIS_SIZE)

        # ось 0Y
        axisY = np.array([[0, 0, 0, 1], [0, self.divisions, 0, 1]])
        pts = np.array(Line(axisY).build()).dot(T)
        self.addItem(pts.tolist(), "Y", QtCore.Qt.green, AXIS_SIZE)

        # ось 0Z
        axisZ = np.array([[0, 0, 0, 1], [0, 0, self.divisions, 1]])
        pts = np.array(Line(axisZ).build()).dot(T)
        self.addItem(pts.tolist(), "Z", QtCore.Qt.blue, AXIS_SIZE)

        # график
        pts = coord.dot(T)
        self.addItem(pts.tolist(), alias, color)

        self.repaint()
