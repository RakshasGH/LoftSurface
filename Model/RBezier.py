# -*- coding: utf-8 -*-

import numpy as np


class RBezier:
    """
    Класс RBezier представляет собой реализацию конического сечения,
    в основе которого лежит рациональная кривая Безье 2-ой степени
    """
    def __init__(self, points, weight=0.5):
        """
        weight -- вес
        points -- вершины задающего треугольника :: numpy.ndarray
        """
        self.w = weight
        self.pt = points

        self.tmin = 0
        self.tmax = 1

    # ==========================================================
    # расчет кривой Безье по указанному параметру
    # ==========================================================
    def calculate(self, t):
        p0 = self.pt[0]
        p1 = self.pt[1]
        p2 = self.pt[2]

        numerator = (1 - t)**2 * p0 + 2 * t * (1 - t) * self.w * p1 + t**2 * p2
        denominator = (1 - t)**2 + 2 * t * (1 - t) * self.w + t**2

        if denominator == 0:
            print("деление на ноль.. t = ", t)
            denominator += 0.00001  # ~

        return numerator / denominator

    # ==========================================================
    # расчет кривой Безье по всем параметрам
    # ==========================================================
    def build(self, number=100):
        points = []

        # минимальное количество точек = 2
        if int(number) <= 1:
            return points

        number -= 1
        step = (self.tmax - self.tmin) / number

        for t in np.arange(self.tmin, self.tmax, step):
            points.append(self.calculate(t).tolist())
        points.append(self.calculate(self.tmax).tolist())

        return points
