# -*- coding: utf-8 -*-

import numpy as np


class Line:
    """
    Класс Line представляет собой реализацию отрезка прямой
    """
    def __init__(self, points):
        """
        points -- границы отрезка :: numpy.ndarray
        """
        self.pt = points

        self.tmin = 0
        self.tmax = 1

    # ==========================================================
    # длина отрезка
    # ==========================================================
    def distance(self):
        P1 = self.pt[0]
        P2 = self.pt[1]

        # если задана одна точка
        if np.array_equal(P1, P2):
            return 0
        else:
            # формула для вычисления расстояния между двумя точками
            return np.sqrt(np.sum(np.power(P2 - P1, 2)))

    # ==========================================================
    # направляющий вектор
    # ==========================================================
    def direction(self):
        P1 = self.pt[0]
        P2 = self.pt[1]

        return P2 - P1

    # ==========================================================
    # расчет прямой по заданному параметру
    # ==========================================================
    def calculate(self, t):
        P1 = self.pt[0]
        P2 = self.pt[1]

        return P1 + (P2 - P1) * t

    # ==========================================================
    # расчет прямой по всем параметрам
    # ==========================================================
    def build(self, number=2):
        points = []

        if number == 1:
            points.append(self.calculate(self.tmin).tolist())
            return points

        number -= 1
        step = (self.tmax - self.tmin) / number

        for t in np.arange(self.tmin, self.tmax, step):
            points.append(self.calculate(t).tolist())
        points.append(self.calculate(self.tmax).tolist())

        return points
