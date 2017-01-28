# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui


class FreemanSettings:
    def __init__(self, controller):
        self.controller = controller
        self.mainLayout = QtWidgets.QVBoxLayout()

        # поле для ввода кода Фримена
        self.edtFreeman = QtWidgets.QLineEdit("000222555")

        # кнопка для отрисовки фигуры по коду Фримена
        self.btnDrawFreeman = QtWidgets.QPushButton("Построить")
        self.btnDrawFreeman.clicked.connect(self.controller.on_clicked_btnDrawFreeman)

        # картинка с обозначениями для кода Фримена
        self.lblImageFreeman = QtWidgets.QLabel()
        self.lblImageFreeman.setPixmap(QtGui.QPixmap("resources/ccgraph.png", "PNG"))

        # поле для задания угла отрицательного поворота
        self.edtNegRotate = QtWidgets.QLineEdit("90")

        # кнопка для выполнения поворота фигуры
        self.btnNegRotate = QtWidgets.QPushButton("Повернуть")
        self.btnNegRotate.clicked.connect(self.controller.on_clicked_btnNegRotate)

        # поле для ввода значения приращения вдоль оси X
        self.edtMove = QtWidgets.QLineEdit("3")

        # кнопка для выполнения перемещения фигуры
        self.btnMove = QtWidgets.QPushButton("Переместить")
        self.btnMove.clicked.connect(self.controller.on_clicked_btnMove)

        # поля для ввода коэффициентов неоднородного масштабирования
        self.edtScalingX = QtWidgets.QLineEdit("-0.5")
        self.edtScalingY = QtWidgets.QLineEdit("1.5")

        # кнопка для выполнения неоднородного масштабирования фигуры
        self.btnScaling = QtWidgets.QPushButton("Масштабировать")
        self.btnScaling.clicked.connect(self.controller.on_clicked_Scaling)

        # флажок для активации пошагового режима
        self.cbMirror = QtWidgets.QCheckBox("Пошаговый режим")
        self.cbMirror.clicked.connect(self.controller.on_clicked_check)

        # кнопка для выполнения отражения относительно прямой y = 6x + 5
        self.btnMirror = QtWidgets.QPushButton("Отразить")
        self.btnMirror.clicked.connect(self.controller.on_clicked_Mirror)

        # кнопка для выполнения комплексного преобразования
        self.btnComplex = QtWidgets.QPushButton("Преобразовать")
        self.btnComplex.clicked.connect(self.controller.on_clicked_Complex)

        # размещение виджетов

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(QtWidgets.QLabel("<i>По рисунку слева задайте<br>фигуру кодом Фримена:</i>"))
        vbox.addWidget(self.edtFreeman)
        vbox.addWidget(self.btnDrawFreeman)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.lblImageFreeman)
        hbox.addLayout(vbox)

        form = QtWidgets.QFormLayout()
        # размеры компонентов будут соответствовать рекомендуемым
        # (возвращаемым методом sizeHint())
        form.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldsStayAtSizeHint)
        # длинные надписи могут находиться выше компонентов, а короткие
        # надписи -- слева от компонентов
        form.setRowWrapPolicy(QtWidgets.QFormLayout.WrapLongRows)
        form.addRow(hbox)
        form.addRow(QtWidgets.QLabel("<b>Отрицательный поворот относительно середины одной из сторон</b>"))
        form.addRow("Угол поворота:", self.edtNegRotate)
        form.addRow(self.btnNegRotate)
        form.addRow(QtWidgets.QLabel("<b>Перенос вдоль оси X</b>"))
        form.addRow("Приращение:", self.edtMove)
        form.addRow(self.btnMove)
        form.addRow(QtWidgets.QLabel("<b>Неоднородное масштабирование</b>"))
        form.addRow("Коэффициент масштабирования по оси X:", self.edtScalingX)
        form.addRow("Коэффициент масштабирования по оси Y:", self.edtScalingY)
        form.addRow(self.btnScaling)
        form.addRow(QtWidgets.QLabel("<b>Отражение относительно прямой y = 6x + 5</b>"))
        form.addRow(self.cbMirror)
        form.addRow(self.btnMirror)
        form.addRow(QtWidgets.QLabel("<b>Комплексное преобразование</b>"))
        form.addRow(self.btnComplex)

        self.mainLayout.addLayout(form)
