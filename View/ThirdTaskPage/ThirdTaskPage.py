# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui
import numpy as np

from Model.Line import Line
from Model.PBSpline import PBSpline
from Model.LoftSurface import LoftSurface
from View.SecondTaskPage.RBezierSettings import RBezierSettings
from View.SecondTaskPage.BSplineSettings import BSplineSettings
from View.SecondTaskPage.PivotTable import PivotTable
from View.ThirdTaskPage.PlotSettings import PlotSettings
from View.ThirdTaskPage.LineSettings import LineSettings

DEFAULT_SPINE_POINTS = np.array([[-16, 1, 0, 1], [16, 1, 0, 1]])
DEFAULT_PROFIL_POINTS = np.array([[0, 0, 0, 1], [4, 5, 0, 1], [8, 0, 0, 1], [12, -5, 0, 1], [16, 0, 0, 1]])
DEFAULT_GUIDE_POINTS = np.array([[-16, 0, 0, 1], [-5, 5, 0, 1], [-4, 4, 0, 1], [-3, 4, 0, 1], [-2, 3, 0, 1],
                                 [0, 0, 0, 1], [1, 1, 0, 1], [2, 2, 0, 1], [3, 3, 0, 1], [3, 4, 0, 1], [3, 6, 0, 1],
                                 [6, 6, 0, 1], [6, 8, 0, 1], [6, 9, 0, 1], [7, 6, 0, 1], [7, 7, 0, 1], [7, 8, 0, 1],
                                 [7, 9, 0, 1], [8, 0, 0, 1]])


class ThirdTaskPage(QtWidgets.QFrame):
    def __init__(self, stack):
        QtWidgets.QFrame.__init__(self)
        self.stack = stack

        self.cache = []
        self.cacheLoft = None

        # используемые виджеты
        self.spineSettings = LineSettings(self, DEFAULT_SPINE_POINTS)
        self.profilSettings = RBezierSettings(self, DEFAULT_PROFIL_POINTS)
        self.profilSettings.btnRBezier.hide()  # виджет не требуется
        self.guideOneSettings = BSplineSettings(self, DEFAULT_GUIDE_POINTS)
        self.guideOneSettings.btnBSpline.hide()  # виджет не требуется
        self.guideTwoSettings = BSplineSettings(self, DEFAULT_GUIDE_POINTS + [0, 0, 6, 0])
        self.guideTwoSettings.btnBSpline.hide()  # виджет не требуется
        self.plotSettings = PlotSettings(self)

        # кнопка для визуализации lofting поверхности на канве
        self.btnLofting = QtWidgets.QPushButton("Построить поверхность")
        self.btnLofting.clicked.connect(self.on_clicked_Lofting)

        # кнопка для возврата в главное меню
        self.btnHome = QtWidgets.QPushButton("На стартовую страницу")
        self.btnHome.clicked.connect(self.on_clicked_btnHome)

        # размещение виджетов

        toolBox = QtWidgets.QToolBox()
        # виджеты профиля (кривая из двух конических сечений)
        widget = QtWidgets.QWidget()
        widget.setLayout(self.profilSettings.mainLayout)
        toolBox.addItem(widget, "Профиль поверхности")
        # виджеты 1-ой образующей (периодический B-сплайн 3-ей степени)
        widget = QtWidgets.QWidget()
        widget.setLayout(self.guideOneSettings.mainLayout)
        toolBox.addItem(widget, "1-ая образующая поверхности")
        # виджеты 2-ой образующей (периодический B-сплайн 3-ей степени)
        widget = QtWidgets.QWidget()
        widget.setLayout(self.guideTwoSettings.mainLayout)
        toolBox.addItem(widget, "2-ая образующая поверхности")
        # виджеты направляющей
        widget = QtWidgets.QWidget()
        widget.setLayout(self.spineSettings.mainLayout)
        toolBox.addItem(widget, "Направляющая поверхности")

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(toolBox)
        vbox.addWidget(self.btnLofting)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addLayout(vbox)
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
    # обработчики незадействованных виджетов
    # ==========================================================
    def on_clicked_Bezier(self):
        pass

    def on_clicked_BSpline(self):
        pass

    # ==========================================================
    # окно выбора цвета для отображения кривой
    # ==========================================================
    def on_clicked_ChooseColor(self):
        btnChooseColor = self.sender()

        color = QtWidgets.QColorDialog.getColor(initial=QtGui.QColor("red"))
        if color.isValid():
            btnChooseColor.setStyleSheet("background-color: {0}".format(color.name()))

    # ==========================================================
    # построить и вывести на экран lofting поверхность
    # ==========================================================
    def on_clicked_Lofting(self):
        # граничные точки направляющей
        table = PivotTable()
        table.load(self.spineSettings.tblViewLinePivots)
        spinePivots = table.points()

        # опорные точки 1-ой образующей
        table = PivotTable()
        table.load(self.guideOneSettings.tblViewBSplinePivots)
        guide1Pivots = table.points()

        # опорные точки 2-ой образующей
        table = PivotTable()
        table.load(self.guideTwoSettings.tblViewBSplinePivots)
        guide2Pivots = table.points()

        # опорные точки кривой для профиля
        table = PivotTable()
        table.load(self.profilSettings.tblViewRBezierPivots)
        profilPivots = table.points()

        # формируем направляющую и образующие
        spine = np.array(Line(spinePivots).build(int(self.spineSettings.edtNumberPoints.value())))
        guide1 = np.array(PBSpline(guide1Pivots).build(50))
        guide2 = np.array(PBSpline(guide2Pivots).build(50))

        # формируем lofting поверхность по заданному профилю
        w1 = float(self.profilSettings.edtRBezierW1.value())
        w2 = float(self.profilSettings.edtRBezierW2.value())
        model = LoftSurface([profilPivots, w1, w2], spine, guide1, guide2)
        loft = model.build()
        loft = np.array(loft)

        # выводим результат на экран
        self.drawLofting(loft, guide1, guide2, spine)

        # сохраняем точки в памяти
        self.cache = [guide1, guide2, spine]
        self.cacheLoft = loft

    # ==========================================================
    # вывод lofting поверхности на экран
    # ==========================================================
    def drawLofting(self, loft, guide1, guide2, spine):
        self.plotSettings.frameCanvas.resetDictDraw()

        # вывод направляющей и образующих на экран
        self.plotSettings.frameCanvas.draw(spine, "spine",
                                           self.spineSettings.btnChooseColorLine.palette().color(
                                               QtGui.QPalette.Background),
                                           self.plotSettings.edtAngleX.value(), self.plotSettings.edtAngleY.value())
        self.plotSettings.frameCanvas.draw(guide1, "guide1",
                                           self.guideOneSettings.btnChooseColorBSpline.palette().color(
                                               QtGui.QPalette.Background),
                                           self.plotSettings.edtAngleX.value(), self.plotSettings.edtAngleY.value())
        self.plotSettings.frameCanvas.draw(guide2, "guide2",
                                           self.guideTwoSettings.btnChooseColorBSpline.palette().color(
                                               QtGui.QPalette.Background),
                                           self.plotSettings.edtAngleX.value(), self.plotSettings.edtAngleY.value())
        # вывод сечений поверхности на экран
        i = 1
        for profil in loft:
            self.plotSettings.frameCanvas.draw(profil, "profil" + str(i),
                                               self.profilSettings.btnChooseColorRBezier.palette().color(
                                                   QtGui.QPalette.Background),
                                               self.plotSettings.edtAngleX.value(), self.plotSettings.edtAngleY.value())
            i += 1

    # ==========================================================
    # пересчитать точки на канве
    # ==========================================================
    def on_value_changed_Angle(self):
        if self.cacheLoft is not None:
            guide1, guide2, spine = self.cache

            self.drawLofting(self.cacheLoft, guide1, guide2, spine)
