from cv2 import fillPoly
from geometry import Buffer, Point
from numpy import array, int32


class Triangle(list):
    def draw(self, image):
        def convert(p: Point):
            return p.tuple()

        pts = array(list(map(convert, self)), int32)
        pts = pts.reshape((-1, 1, 2))
        fillPoly(image, [pts], (100, 0, 0))

    def __contains__(self, coords):
        def sign(p1: Point, p2: Point, p3: Point):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

        d1 = sign(Point(coords), self[0], self[1])
        d2 = sign(Point(coords), self[1], self[2])
        d3 = sign(Point(coords), self[2], self[0])

        has_pos = d1 > 0 or d2 > 0 or d3 > 0
        has_neg = d1 < 0 or d2 < 0 or d3 < 0
        return not (has_neg and has_pos)

    def output(self, points: list):
        z_plus = []
        z_minus = []
        for p in self:
            if p in points:
                i = 2*points.index(p)
                z_plus.append(str(i))
                z_minus.append(str(i+1))
        return ','.join(z_plus)+','+','.join(z_minus)


class ListOfTriangles(list):
    def draw(self, image):
        for t in self:
            t.draw(image)

    def output(self, points):
        output = []
        for t in self:
            output.append(t.output(points))
        return ','.join(output)

    def add_new_triangle(self, buffer: Buffer):
        new = Triangle()
        for p in buffer:
            new.append(p)
        buffer.clear()
        self.append(new)

    def delete(self, coords: tuple):
        for t in self:
            if coords in t:
                self.remove(t)
                return True
        return False


