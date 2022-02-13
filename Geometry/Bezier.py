from math import comb
from cv2 import line
from numpy import arange
from geometry.Buffer import Buffer

class BezierCurve(list):
    def __init__(self):
        super().__init__()

    def bezier(self, image):
        def curve(t):
            n = len(self) - 1
            x = 0
            y = 0
            for i, p in enumerate(self):
                b = comb(n, i) * (t ** i) * ((1 - t) ** (n - i))
                x += b * p.x
                y += b * p.y
            return round(x), round(y)

        for t in arange(0, 1, 0.01):
            line(image, curve(t), curve(t + 0.01), (255, 255, 255), 1)


class Bezier(list):
    def __init__(self):
        super().__init__()

    def draw(self, image):
        for bc in self:
            bc.bezier(image)

    def add_new_curve(self, buffer: Buffer):
        new = BezierCurve()
        for p in buffer:
            new.append(p)
        buffer.clear()
        self.append(new)