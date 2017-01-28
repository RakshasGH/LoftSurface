# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from View.SecondTaskPage.PivotTable import PivotTable


class RBezierSettings:
    def __init__(self, controller, pivots):
        self.controller = controller
        self.mainLayout = QtWidgets.QVBoxLayout()

        # кнопка для вызова окна выбора цвета
        self.btnChooseColorRBezier = QtWidgets.QPushButton()
        self.btnChooseColorRBezier.setStyleSheet("background-color: red")
        self.btnChooseColorRBezier.clicked.connect(self.controller.on_clicked_ChooseColor)

        # поля для ввода весов кривой из двух конических сечений
        self.edtRBezierW1 = QtWidgets.QDoubleSpinBox()
        self.edtRBezierW2 = QtWidgets.QDoubleSpinBox()
        for edtRBezierW in self.edtRBezierW1, self.edtRBezierW2:
            edtRBezierW.setValue(0.5)
            edtRBezierW.setDecimals(1)
            edtRBezierW.setSingleStep(0.1)
            edtRBezierW.setRange(-1000, 1000)

        # таблица с координатами
        table = PivotTable()
        self.tblViewRBezierPivots = table.create(pivots)

        # кнопка для построения графика на экране
        self.btnRBezier = QtWidgets.QPushButton("Построить")
        self.btnRBezier.clicked.connect(self.controller.on_clicked_Bezier)

        # размещение виджетов

        form = QtWidgets.QFormLayout()
        # размеры компонентов будут соответствовать рекомендуемым
        # (возвращаемым методом sizeHint())
        form.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldsStayAtSizeHint)
        # длинные надписи могут находиться выше компонентов, а короткие
        # надписи -- слева от компонентов
        form.setRowWrapPolicy(QtWidgets.QFormLayout.WrapLongRows)
        form.addRow("Вес 1-го конического сечения:", self.edtRBezierW1)
        form.addRow("Вес 2-го конического сечения:", self.edtRBezierW2)
        form.addRow("Цвет кривой на графике:", self.btnChooseColorRBezier)

        self.mainLayout.addLayout(form)
        self.mainLayout.addWidget(QtWidgets.QLabel("Таблица с координатами опорных точек:"))
        self.mainLayout.addWidget(self.tblViewRBezierPivots)
        self.mainLayout.addWidget(self.btnRBezier)
