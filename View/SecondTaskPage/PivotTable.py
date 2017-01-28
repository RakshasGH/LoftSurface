# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui
import numpy as np


class PivotTable:
    """
    Вспомогательный класс для работы с QTableView
    """
    def __init__(self):
        self.table = QtWidgets.QTableView()
        self.model = QtGui.QStandardItemModel()

    def create(self, points):
        dimension = points.shape[1]  # число координат точки

        # проход по точкам
        for row in range(0, points.shape[0]):
            for column in range(0, dimension):
                item = QtGui.QStandardItem("{0}".format(points[row][column]))
                self.model.setItem(row, column, item)

        labels = ["x", "y", "z", "h"]
        self.model.setHorizontalHeaderLabels(labels[:dimension])

        self.table.setModel(self.model)
        return self.table

    def load(self, table):
        self.table = table
        self.model = table.model()

    def count(self):
        return self.model.rowCount()

    def points(self):
        res = np.empty((self.model.rowCount(), self.model.columnCount()))
        dimension = res.shape[1]  # число координат точки

        for row in range(self.model.rowCount()):
            for column in range(0, dimension):
                index = self.model.index(row, column)
                res[row][column] = float(self.model.data(index))

        return res
