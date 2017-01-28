# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui
import numpy as np

from View.SecondTaskPage.RBezierSettings import RBezierSettings
from View.SecondTaskPage.BSplineSettings import BSplineSettings
from View.SecondTaskPage.PlotSettings import PlotSettings
from View.SecondTaskPage.PivotTable import PivotTable
from Model.RBezier import RBezier
from Model.PBSpline import PBSpline

DEFAULT_BEZIER_POINTS = np.array([[-8, 0, 0], [-4, 5, 0], [0, 0, 0], [4, -5, 0], [8, 0, 0]])
DEFAULT_SPLINE_POINTS = np.array([[-8, 0, 0], [-5, -5, 0], [-4, -4, 0], [-3, -4, 0], [-2, -3, 0], [0, 0, 0],
                                  [1, 1, 0], [2, 2, 0], [3, 3, 0], [3, 4, 0], [3, 6, 0], [6, 6, 0], [6, 8, 0],
                                  [6, 9, 0], [7, 6, 0], [7, 7, 0], [7, 8, 0], [7, 9, 0], [8, 0, 0]])


class SecondTaskPage(QtWidgets.QFrame):
    def __init__(self, stack):
        QtWidgets.QFrame.__init__(self)
        self.stack = stack

        # используемые виджеты
        self.rbezierSettings = RBezierSettings(self, DEFAULT_BEZIER_POINTS[:, :2])
        self.bsplineSettings = BSplineSettings(self, DEFAULT_SPLINE_POINTS[:, :2])
        self.plotSettings = PlotSettings(self)

        # кнопка для возврата в главное меню
        self.btnHome = QtWidgets.QPushButton("На стартовую страницу")
        self.btnHome.clicked.connect(self.on_clicked_btnHome)

        # размещение виджетов

        toolBox = QtWidgets.QToolBox()
        # виджеты для кривой из двух конических сечений
        widget = QtWidgets.QWidget()
        widget.setLayout(self.rbezierSettings.mainLayout)
        toolBox.addItem(widget, "Кривая из двух конических сечений")
        # виджеты для периодического B-сплайна 3-ей степени
        widget = QtWidgets.QWidget()
        widget.setLayout(self.bsplineSettings.mainLayout)
        toolBox.addItem(widget, "Периодический B-сплайн 3-ей степени")

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(toolBox, stretch=0)
        hbox.addLayout(self.plotSettings.mainLayout, stretch=1)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.btnHome)

        self.setLayout(vbox)

    # ==========================================================
    # возврат в главное меню
    # ==========================================================
    def on_clicked_btnHome(self):
        self.stack.setCurrentIndex(0)

    # ==========================================================
    # расчет и вывод на экран кривой из двух конических сечений
    # ==========================================================
    def on_clicked_Bezier(self):
        table = PivotTable()
        table.load(self.rbezierSettings.tblViewRBezierPivots)

        pts = table.points()
        w = [float(self.rbezierSettings.edtRBezierW1.value()), float(self.rbezierSettings.edtRBezierW2.value())]
        i = 0
        for pt in pts[:3], pts[2:]:
            model = RBezier(pt, w[i])
            i += 1

            # задающий треугольник
            coord = []
            for p in pt.tolist():
                coord.append(p)
            self.plotSettings.frameCanvas.draw(coord, "Triangle" + str(i), QtCore.Qt.cyan,
                                               bVisible=self.plotSettings.cbDrawBezier.isChecked())

            # коническое сечение
            coord = (model.build())
            self.plotSettings.frameCanvas.draw(coord, "RBezier" + str(i),
                                               self.rbezierSettings.btnChooseColorRBezier.palette().color(
                                                   QtGui.QPalette.Background),
                                               bVisible=self.plotSettings.cbDrawBezier.isChecked())

    # ==========================================================
    # расчет и вывод на экран периодического B-сплайна
    # ==========================================================
    def on_clicked_BSpline(self):
        table = PivotTable()
        table.load(self.bsplineSettings.tblViewBSplinePivots)

        pts = table.points()
        p = int(self.bsplineSettings.combBSpline.itemText(self.bsplineSettings.combBSpline.currentIndex()))
        model = PBSpline(pts, p)
        coord = model.build()

        self.plotSettings.frameCanvas.draw(coord, "BSpline", self.bsplineSettings.btnChooseColorBSpline.palette().color(QtGui.QPalette.Background),
                                           bVisible=self.plotSettings.cbDrawBSpline.isChecked())

    # ==========================================================
    # окно выбора цвета для отображения кривой
    # ==========================================================
    def on_clicked_ChooseColor(self):
        btnChooseColor = self.sender()

        color = QtWidgets.QColorDialog.getColor(initial=QtGui.QColor("red"))
        if color.isValid():
            btnChooseColor.setStyleSheet("background-color: {0}".format(color.name()))

    # ==========================================================
    # очистить канву
    # ==========================================================
    def on_clicked_btnClearCanvas(self):
        self.plotSettings.frameCanvas.resetDictDraw()
        self.plotSettings.frameCanvas.drawAllItems()

    # ==========================================================
    # настройки канвы для кривой из двух конических сечений
    # ==========================================================
    def on_clicked_cbDrawBezier(self):
        for i in range(1, 3):
            self.plotSettings.frameCanvas.setVisibleItem("RBezier" + str(i), self.plotSettings.cbDrawBezier.isChecked())
            self.plotSettings.frameCanvas.setVisibleItem("Triangle" + str(i), self.plotSettings.cbDrawBezier.isChecked())
        self.plotSettings.frameCanvas.drawAllItems()

    # ==========================================================
    # настройки канвы для периодического B-сплайна
    # ==========================================================
    def on_clicked_cbDrawBSpline(self):
        self.plotSettings.frameCanvas.setVisibleItem("BSpline", self.plotSettings.cbDrawBSpline.isChecked())
        self.plotSettings.frameCanvas.drawAllItems()
