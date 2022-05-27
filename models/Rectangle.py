from __future__ import annotations


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h

    def isOverlapped(self, rect: Rectangle):
        L, R, T, B = False, False, False, False

        # ЛВ между верхними
        if rect.x <= self.x <= rect.x + rect.w:
            L = True

        # ПВ между верхними
        if rect.x <= self.x + self.w <= rect.x + rect.w:
            R = True

        # Верхние между боковыми
        if rect.y <= self.y <= rect.y + rect.h:
            T = True

        # Нижние между боковыми
        if rect.y <= self.y + self.h <= rect.y + rect.h:
            B = True

        if L and R and T and B:
            return True
        else:
            return False
