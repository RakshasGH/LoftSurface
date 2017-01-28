# -*- coding: utf-8 -*-

from View.Plot.Plot2D import Plot2D


class Plot2DWithInfo(Plot2D):
    """
    Класс PlotWithInfo предоставляет функционал для
    визуализации двумерных графиков на экране с возможностью
    записи в указанный QLabel информации о позиции мыши
    """
    def __init__(self, label):
        Plot2D.__init__(self)

        self.setMouseTracking(True)
        self.lblPos = label

    def mouseMoveEvent(self, e):
        pt = e.localPos()
        pt = self.convert_to_coord(pt.x(), pt.y())
        self.lblPos.setText("[{0:.3f}; {1:.3f}]".format(pt[0], pt[1]))
