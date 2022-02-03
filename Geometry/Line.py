from Geometry.Point import Point


class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def __contains__(self, item: Point):
        return self.point1 == item or self.point2 == item

    def __eq__(self, other):
        return self.point1 in other and self.point2 in other

    def __str__(self):
        return f'({str(self.point1)},{str(self.point2)})'

    def __sub__(self, other):
        if self.point1 == other.point1:
            return Line(self.point2, other.point2)
        elif self.point1 == other.point2:
            return Line(self.point2, other.point1)
        elif self.point2 == other.point1:
            return Line(self.point1, other.point2)
        elif self.point2 == other.point2:
            return Line(self.point1, other.point1)
        raise NotImplementedError

    def is_connected_to(self, line):
        if self != line:
            return self.point1 in line or self.point2 in line
        return False
