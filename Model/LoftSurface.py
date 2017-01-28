# -*- coding: utf-8 -*-

from Model.Line import Line
from Model.RBezier import RBezier
import numpy as np


class LoftSurface:
    """
    Класс LoftSurface представляет собой реализацию
    lofting поверхности следующей конфигурации:
    * масштабирование -- общее
    * направляющая -- отрезок прямой
    * профиль -- кривая из двух конических сечений
    """
    def __init__(self, profil, spine, guide1, guide2):
        """
        profil :: list
        spine :: numpy.ndarray
        guide1 :: numpy.ndarray
        guide2 :: numpy.ndarray
        """
        self.profil = profil[0]
        self.weight = profil[1:]

        self.spine = spine
        self.guide1 = guide1
        self.guide2 = guide2

    # ==========================================================
    # определяет, пересекается ли отрезок с плоскостью
    # ==========================================================
    def isIntersect(self, points, pointOnPlane, normalVector):
        """
        points -- границы отрезка
        pointOnPlane -- точка, лежащая в плоскости
        normalVector -- нормальный вектор к плоскости

        pointOnPlane и normalVector определяют положение плоскости в пространстве
        normalVector = (A; B; C)
        pointOnPlane = (x1, y1, z1)
        """
        M1, M2 = points[0], points[1]

        # A(x - x1) + B(y - y1) + C(z - z1) = 0
        expr1 = normalVector.dot((M1 - pointOnPlane).transpose())
        expr2 = normalVector.dot((M2 - pointOnPlane).transpose())

        # взаимное расположение пары точек M1 и M2 относительно плоскости
        if expr1 > 0 and expr2 > 0 or expr1 < 0 and expr2 < 0:
            return False
        else:
            return True

    # ==========================================================
    # возвращает точки пересечения кривой и плоскости
    # ==========================================================
    def getIntersect(self, curve, pointOnPlane, normalVector):
        points = []

        # свободный член уравнения плоскости
        # D = -(A * x1 + B * y1 + C * z1)
        D = -normalVector.dot(pointOnPlane.transpose())

        ptStart = curve[0]
        for ptEnd in curve[1:]:
            if self.isIntersect([ptStart, ptEnd], pointOnPlane, normalVector):
                # точка пересечения прямой с плоскостью
                segment = Line([ptStart, ptEnd])  # рассматриваемый отрезок
                direction = segment.direction()  # направляющий вектор отрезка

                # решение системы уравнений
                numerator = normalVector.dot(ptStart.transpose()) + D
                denominator = normalVector.dot(direction.transpose())

                # если отрезок и плоскость не параллельны друг другу
                if denominator != 0:
                    # находим координаты точки пересечения отрезка с плоскостью
                    t = -(numerator / denominator)
                    points.append(segment.calculate(t).tolist())
                else:
                    if numerator == 0:
                        # отрезок лежит в данной плоскости
                        pass
                    else:
                        # отрезок и плоскость параллельны друг другу
                        # (условие не наступит, т. к. предварительно проведена проверка)
                        pass
            ptStart = ptEnd

        return points

    # ==========================================================
    # пересчет координат точки из локальной СК в глобальную СК
    # ==========================================================
    def recalcLocalPoint(self, localPoint, originPoint, xBasis, yBasis, zBasis):
        # матрица перехода от базиса глобальной СК к базису локальной СК
        A = np.matrix([[xBasis.item(0), yBasis.item(0), zBasis.item(0)],
                       [xBasis.item(1), yBasis.item(1), zBasis.item(1)],
                       [xBasis.item(2), yBasis.item(2), zBasis.item(2)]])

        globalPoint = A.dot(localPoint) + originPoint
        return globalPoint

    # ==========================================================
    # пересчет координат точки из глобальной СК в локальную СК
    # (метод не используется, реализован на всякий пожарный)
    # ==========================================================
    def recalcGlobalPoint(self, globalPoint, originPoint, xBasis, yBasis, zBasis):
        # матрица перехода от базиса глобальной СК к базису локальной СК
        A = np.matrix([[xBasis.item(0), yBasis.item(0), zBasis.item(0)],
                       [xBasis.item(1), yBasis.item(1), zBasis.item(1)],
                       [xBasis.item(2), yBasis.item(2), zBasis.item(2)]])
        AInv = np.linalg.inv(A)

        localPoint = AInv.dot(globalPoint - originPoint)
        return localPoint

    # ==========================================================
    # расчет точек lofting поверхности
    # ==========================================================
    def build(self):
        points = []

        # обход точек направляющей
        for currPt in self.spine:
            pointOnPlane = currPt
            normalVector = Line(self.spine)

            # поиск точек пересечения guide с плоскостью сечения
            intersectionPoints1 = np.array(self.getIntersect(self.guide1, pointOnPlane, normalVector.direction()))
            intersectionPoints2 = np.array(self.getIntersect(self.guide2, pointOnPlane, normalVector.direction()))

            if len(intersectionPoints1) == 1 and len(intersectionPoints2) == 1:
                profilLine = Line([intersectionPoints1, intersectionPoints2])  # основание профиля

                # вычисляем масштабный коэффициент
                M = profilLine.distance()
                if M == 0:  # случай пересечения guide кривых
                    continue

                # единичный направляющий вектор направляющей
                spineBasis = normalVector.direction() / normalVector.distance()
                spineBasis = np.delete(spineBasis, 3)  # исключаем 4-ю координату

                # единичный направляющий вектор основания профиля
                profilBasisX = profilLine.direction() / profilLine.distance()
                profilBasisX = np.delete(profilBasisX, 3)  # исключаем 4-ю координату

                # единичный направляющий вектор высоты профиля (результат векторного произведения)
                profilBasisY = np.cross(spineBasis, profilBasisX) * -1  # направление вектора -- вверх

                # начало локальной СК
                O = np.delete(intersectionPoints1, 3)  # исключаем 4-ю координату

                pts = self.profil[:, :3]  # (x, y, z)-координаты опорных точек объекта для профиля
                X = Line([pts[0], pts[4]]).distance()  # длина основания объекта для профиля
                pts = pts * M / X  # выполняем общее масштабирование

                # формирование точек кривой из двух конических сечений
                i = 0
                for ptsRBezier in pts[:3, :3], pts[2:, :3]:
                    res = []
                    for pt in ptsRBezier:
                        # пересчет координат точек
                        vertex = self.recalcLocalPoint(pt, O, profilBasisX, profilBasisY, spineBasis)
                        vertex = np.squeeze(np.asarray(vertex))
                        vertex = np.hstack([vertex, [1]])  # добавляем 4-ю координату
                        res.append(vertex.tolist())

                    profil = RBezier(np.array(res), self.weight[i]).build(50)
                    points.append(profil)
                    i += 1

        return points
