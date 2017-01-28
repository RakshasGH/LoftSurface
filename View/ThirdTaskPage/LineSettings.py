# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from View.SecondTaskPage.PivotTable import PivotTable


class LineSettings:
    def __init__(self, controller, pivots):
        self.controller = controller
        self.mainLayout = QtWidgets.QVBoxLayout()

        # поле для ввода количества точек прямой
        self.edtNumberPoints = QtWidgets.QSpinBox()
        self.edtNumberPoints.setRange(2, 500)
        self.edtNumberPoints.setValue(50)

        # кнопка для вызова окна выбора цвета
        self.btnChooseColorLine = QtWidgets.QPushButton()
        self.btnChooseColorLine.setStyleSheet("background-color: gray")
        self.btnChooseColorLine.clicked.connect(self.controller.on_clicked_ChooseColor)

        # таблица с координатами
        table = PivotTable()
        self.tblViewLinePivots = table.create(pivots)

        # размещение виджетов

        form = QtWidgets.QFormLayout()
        # размеры компонентов будут соответствовать рекомендуемым
        # (возвращаемым методом sizeHint())
        form.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldsStayAtSizeHint)
        # длинные надписи могут находиться выше компонентов, а короткие
        # надписи -- слева от компонентов
        form.setRowWrapPolicy(QtWidgets.QFormLayout.WrapLongRows)
        form.addRow("Количество точек прямой: ", self.edtNumberPoints)
        form.addRow("Цвет прямой на графике: ", self.btnChooseColorLine)

        self.mainLayout.addLayout(form)
        self.mainLayout.addWidget(QtWidgets.QLabel("Таблица с координатами границ прямой:"))
        self.mainLayout.addWidget(self.tblViewLinePivots)
