# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from View.SecondTaskPage.PivotTable import PivotTable


class BSplineSettings:
    def __init__(self, controller, pivots):
        self.controller = controller
        self.mainLayout = QtWidgets.QVBoxLayout()

        # виджет для выбора степени B-сплайна из заданного списка
        self.combBSpline = QtWidgets.QComboBox()
        for i in range(1, 4):
            self.combBSpline.addItem(str(i))
        self.combBSpline.setCurrentIndex(2)

        # кнопка для вызова окна выбора цвета
        self.btnChooseColorBSpline = QtWidgets.QPushButton()
        self.btnChooseColorBSpline.setStyleSheet("background-color: blue")
        self.btnChooseColorBSpline.clicked.connect(self.controller.on_clicked_ChooseColor)

        # поле для указания количества опорных точек
        self.edtNumberPivots = QtWidgets.QSpinBox()
        self.edtNumberPivots.setRange(19, 100)

        # таблица с координатами
        table = PivotTable()
        self.tblViewBSplinePivots = table.create(pivots)

        # кнопка для построения графика на экране
        self.btnBSpline = QtWidgets.QPushButton("Построить")
        self.btnBSpline.clicked.connect(self.controller.on_clicked_BSpline)

        # размещение виджетов

        form = QtWidgets.QFormLayout()
        # размеры компонентов будут соответствовать рекомендуемым
        # (возвращаемым методом sizeHint())
        form.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldsStayAtSizeHint)
        # длинные надписи могут находиться выше компонентов, а короткие
        # надписи -- слева от компонентов
        form.setRowWrapPolicy(QtWidgets.QFormLayout.WrapLongRows)
        form.addRow("Степень кривой: ", self.combBSpline)
        form.addRow("Цвет кривой на графике: ", self.btnChooseColorBSpline)
        form.addRow("Количество опорных точек: ", self.edtNumberPivots)

        self.mainLayout.addLayout(form)
        self.mainLayout.addWidget(QtWidgets.QLabel("Таблица с координатами опорных точек:"))
        self.mainLayout.addWidget(self.tblViewBSplinePivots)
        self.mainLayout.addWidget(self.btnBSpline)
