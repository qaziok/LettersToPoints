from geometry.Point import Point
from copy import deepcopy


class ListOfPoints(list):
    def add(self, coords: tuple, check_range=20):
        point = Point(coords)
        if len(self):
            for p in self:
                if p.is_near(coords, check_range=check_range):
                    return p
            self.append(point)
            return point
        else:
            self.append(point)
            return point

    def delete(self, coords: tuple):
        for p in self:
            if p.is_near(coords):
                ret = deepcopy(p)
                self.remove(p)
                return ret
        return None

    def check(self, coords):
        for p in self:
            if p.is_near(coords):
                return p
        return None

    def normalize(self):
        dist = 5
        for point1 in self:
            for point2 in self:
                if point1.x - dist < point2.x < point1.x + dist:
                    point2.x = point1.x
                if point1.y - dist < point2.y < point1.y + dist:
                    point2.y = point1.y

    def scale(self, scale):
        for p in self:
            p.rescale(scale)

    def draw(self,image):
        for p in self:
            p.draw(image)

    def desmos(self):
        to_marge = []
        for p in self:
            to_marge.append(f'({p.x},{-p.y})')
        print(','.join(to_marge))
