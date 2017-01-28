# -*- coding: utf-8 -*-

from Model.Transformation import Transformation
import numpy as np


class Freeman:
    """
    Класс Freeman предоставляет методы,
    позволяющие выполнять афинные преобразования
    над множеством вершин, заданных кодом Фримена
    """
    def __init__(self, xStart=0, yStart=0, freeman=""):
        self.abc = self.freeman_to_vertex(freeman, xStart, yStart)  # вершины заданной фигуры

    # ==========================================================
    # интерпретация числа в соответствии с кодом Фримена
    # ==========================================================
    def calcDelta(self, number):
        if number == 0:
            return 1, 0
        if number == 1:
            return 1, 1
        if number == 2:
            return 0, 1
        if number == 3:
            return -1, 1
        if number == 4:
            return -1, 0
        if number == 5:
            return -1, -1
        if number == 6:
            return 0, -1
        if number == 7:
            return 1, -1
        return 0, 0

    # ==========================================================
    # формирование матрицы вершин по коду Фримена
    # ==========================================================
    def freeman_to_vertex(self, sCode, xStart=0, yStart=0):
        if sCode.isdigit():
            vertex = np.matrix([xStart, yStart])
            sCurr = sCode[0]
            x, y = xStart, yStart
            dx, dy = self.calcDelta(int(sCurr))
            for i in range(len(sCode)):
                if sCode[i] == sCurr:
                    x += dx
                    y += dy
                else:
                    vertex = np.vstack([vertex, [x, y]])
                    sCurr = sCode[i]
                    dx, dy = self.calcDelta(int(sCurr))
                    x += dx
                    y += dy
            vertex = np.vstack([vertex, [x, y]])

            # добавляем столбцы для формирования матрицы 4 x 4
            rows = len(vertex)
            vertex = np.c_[vertex, np.zeros(rows)]
            vertex = np.c_[vertex, np.ones(rows)]

            return vertex
        else:
            return None

    # ==========================================================
    # отрицательный поворот на angle градусов
    # относительно середины одной из сторон
    # ==========================================================
    def NegRotate(self, angle=0):
        """
        angle -- угол поворота в градусах
        """
        if self.abc is not None:
            midpt = (self.abc[0] + self.abc[1]) / 2

            # перенос средней точки в начало координат
            T1 = Transformation.getTransferMatrix(-midpt.item(0), -midpt.item(1), -midpt.item(2))

            # отрицательный поворот на угол theta
            theta = -np.deg2rad(angle)
            T2 = Transformation.getRotateZMatrix(theta)

            # перенос средней точки на исходную позицию
            T1Inv = np.linalg.inv(T1)

            # комплексное преобразование
            return self.abc.dot(T1).dot(T2).dot(T1Inv)

    # ==========================================================
    # перенос вдоль оси x на dx единиц
    # ==========================================================
    def Move(self, dx=0):
        """
        dx -- приращение по оси x
        """
        if self.abc is not None:
            # перенос вдоль оси x
            T = Transformation.getTransferMatrix(dx)
            return self.abc.dot(T)

    # ==========================================================
    # неоднородное (локальное) масштабирование
    # ==========================================================
    def Scaling(self, kx=1, ky=1, kz=1):
        """
        kx -- коэффициент масштабирования по оси x
        ky -- коэффициент масштабирования по оси y
        """
        if self.abc is not None:
            # неоднородное масштабирование
            T = Transformation.getScaleMatrix(kx, ky, kz)
            return self.abc.dot(T)

    # ==========================================================
    # прямая вида: y = kx + b
    # заданная прямая -- y = 6x + 5
    # ==========================================================
    def func_line(self, x):
        return 6 * x + 5

    # ==========================================================
    # отражение относительно прямой y = kx + b
    # ==========================================================
    def Mirror(self, key=4):
        if self.abc is not None:
            # смещение к началу координат на b единиц
            b = self.func_line(0)
            T = Transformation.getTransferMatrix(dy=-b)
            if key == 0:
                return self.abc.dot(T)

            # поворот для совмещения заданной прямой с осью y
            x = 1
            y = self.func_line(x) - b
            theta = np.deg2rad(90) - np.arctan(y / x)
            R = Transformation.getRotateZMatrix(theta)
            if key == 1:
                return self.abc.dot(T).dot(R)

            # отражение относительной преобразованной прямой
            O = Transformation.getMirrorYZMatrix()
            if key == 2:
                return self.abc.dot(T).dot(R).dot(O)

            # исходный наклон заданной прямой
            RInv = np.linalg.inv(R)
            if key == 3:
                return self.abc.dot(T).dot(R).dot(O).dot(RInv)

            # исходное положение заданной прямой
            TInv = np.linalg.inv(T)
            return self.abc.dot(T).dot(R).dot(O).dot(RInv).dot(TInv)
