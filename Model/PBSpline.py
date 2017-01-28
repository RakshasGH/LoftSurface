# -*- coding: utf-8 -*-

import numpy as np


class PBSpline:
    """
    Класс PBSpline представляет собой реализацию периодического B-сплайна
    """
    def __init__(self, points, power=3):
        """
        power -- степень периодического B-сплайна
        points -- опорные точки :: numpy.ndarray
        """
        self.p = power  # степень периодического B-сплайна = k - 1
        self.pt = points  # опорные точки

        self.k = self.p + 1  # порядок
        self.ptCount = self.pt.shape[0]  # число опорных точек = n + 1
        n = self.ptCount - 1
        self.X = range(0, n + self.p + 2)  # узловой вектор для периодического B-сплайна

        interval = n - (self.p - 1)  # число существенных интервалов
        self.tmin = self.p
        self.tmax = self.tmin + interval

    # ==========================================================
    # нормализованная функция базиса B-сплайна
    # ==========================================================
    def N(self, i, k, t):
        """
        i = [1; n + 1] -- номер опорной точки
        k -- порядок
        """
        # формула Кокса-де Бура
        if k == 1:
            if self.X[i - 1] <= t < self.X[i + 1 - 1]:
                return 1
            else:
                return 0
        else:
            numerator1 = (t - self.X[i - 1]) * self.N(i, k - 1, t)
            denominator1 = self.X[i + k - 1 - 1] - self.X[i - 1]

            numerator2 = (self.X[i + k - 1] - t) * self.N(i + 1, k - 1, t)
            denominator2 = self.X[i + k - 1] - self.X[i + 1 - 1]

            # считается, что 0 / 0 = 0
            if denominator1 == 0 and denominator2 == 0:
                return 0
            elif denominator1 == 0 and denominator2 != 0:
                return numerator2 / denominator2
            elif denominator1 != 0 and denominator2 == 0:
                return numerator1 / denominator1
            else:
                return numerator1 / denominator1 + numerator2 / denominator2

    # ==========================================================
    # расчет периодического B-сплайна по указанному параметру
    # ==========================================================
    def calculate(self, t):
        number = self.pt.shape[1]  # количество координат у точки

        point = np.zeros(number)  # инициализируем координаты нулями
        for i in range(self.ptCount):
            point = point + self.pt[i] * self.N(i + 1, self.k, t)
        return point

    # ==========================================================
    # расчет периодического B-сплайна по всем параметрам
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
