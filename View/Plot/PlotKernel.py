# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui

DIVISIONS = 15
GRID_COLOR = QtCore.Qt.lightGray
AXIS_COLOR = QtCore.Qt.black


class PlotKernel(QtWidgets.QWidget):
    """
    Класс PlotKernel предоставляет методы для графопостроителей
    """
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.divisions = DIVISIONS
        self.gridColor = GRID_COLOR
        self.axis_color = AXIS_COLOR

        self.axis_y = self.height() / 2
        self.axis_x = self.width() / 2
        self.cell_x = self.axis_x / self.divisions
        self.cell_y = self.axis_y / self.divisions

        self.dictDraw = {}  # словарь с элементами для рисования

    def resizeEvent(self, e):
        self.axis_y = self.height() / 2
        self.axis_x = self.width() / 2
        self.cell_x = self.axis_x / self.divisions
        self.cell_y = self.axis_y / self.divisions

    # ==========================================================
    # из СК в углу
    # ==========================================================
    def convert_to_coord(self, x, y):
        _x = (x - self.axis_x) / self.cell_x
        _y = (self.axis_y - y) / self.cell_y
        return _x, _y

    # ==========================================================
    # к СК в углу
    # ==========================================================
    def convert_from_coord(self, x, y):
        _x = x * self.cell_x + self.axis_x
        _y = y * self.cell_y + self.axis_y
        return _x, _y

    # ==========================================================
    # из СК задачи в пиксели (относительно середины)
    # ==========================================================
    def convert_point(self, x, y):
        _x = x * self.cell_x
        _y = -y * self.cell_y
        return _x, _y

    # ==========================================================
    # добавить элемент для рисования
    # ==========================================================
    def addItem(self, coord, alias, color, size=2, bVisible=True):
        pixels = QtGui.QPolygon()
        for pt in coord:
            v = self.convert_point(pt[0], pt[1])
            pixels.append(QtCore.QPoint(v[0], v[1]))

        pen = QtGui.QPen(color, size)
        self.dictDraw[alias] = [pixels, pen, bVisible]

    # ==========================================================
    # установить состояние элемента для рисования (вкл\выкл)
    # ==========================================================
    def setVisibleItem(self, alias, bValue):
        if alias in self.dictDraw:
            self.dictDraw[alias][2] = bValue

    # ==========================================================
    # удалить элемент для рисования
    # ==========================================================
    def delItem(self, alias):
        try:
            del self.dictDraw[alias]
        except KeyError:
            pass

    # ==========================================================
    # очистка словаря с элементами для рисования
    # ==========================================================
    def resetDictDraw(self):
        self.dictDraw.clear()

    # ==========================================================
    # отрисовать все активные элементы из
    # словаря с элементами для рисования
    # ==========================================================
    def drawAllItems(self):
        self.repaint()
