# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui
from View.Plot.PlotKernel import PlotKernel


class Plot2D(PlotKernel):
    """
    Класс Plot2D реализует функционал для
    визуализации двумерных графиков на экране
    """
    def __init__(self):
        PlotKernel.__init__(self)

    def paintEvent(self, e):
        canvas = QtGui.QPainter(self)
        # canvas.setRenderHint(QtGui.QPainter.Antialiasing)
        canvas.translate(self.axis_x, self.axis_y)

        # рисуем сетку
        canvas.setPen(QtGui.QPen(self.gridColor, 1))
        for i in range(-self.divisions, self.divisions + 1):  # 0
            start_pt = self.convert_point(-self.divisions, i)
            end_pt = self.convert_point(self.divisions, i)
            canvas.drawLine(QtCore.QPoint(start_pt[0], start_pt[1]), QtCore.QPoint(end_pt[0], end_pt[1]))

            start_pt = self.convert_point(i, -self.divisions)
            end_pt = self.convert_point(i, self.divisions)
            canvas.drawLine(QtCore.QPoint(start_pt[0], start_pt[1]), QtCore.QPoint(end_pt[0], end_pt[1]))

        # рисуем координатные оси
        canvas.setPen(QtGui.QPen(self.axis_color, 3))
        canvas.drawLine(QtCore.QPoint(-self.axis_x, 0), QtCore.QPoint(self.axis_x, 0))
        canvas.drawLine(QtCore.QPoint(0, -self.axis_y), QtCore.QPoint(0, self.axis_y))

        # отрисовываем активные элементы
        for figure in self.dictDraw.items():
            if figure[1][2]:  # bVisible
                canvas.setPen(figure[1][1])  # pen
                canvas.drawPolyline(figure[1][0])  # pixels

    # ==========================================================
    # построить график по заданным точкам
    # ==========================================================
    def draw(self, coord, alias="", color=QtCore.Qt.black, size=2, bVisible=True):
        """
        coord :: list
        """
        self.addItem(coord, alias, color, size, bVisible)

        self.repaint()
