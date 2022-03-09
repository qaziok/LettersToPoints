from math import comb
from cv2 import line
from numpy import arange
from geometry import Buffer


class Ellipse:
    def __init__(self, middle, ax, ay):
        self.middle = middle
        self.ax = ax
        self.ay = ay

    def __contains__(self, point: tuple):
        x = point[0] - self.middle[0]
        y = point[1] - self.middle[1]
        return (x * self.ay) ** 2 + (y * self.ax) ** 2 <= (self.ax * self.ay) ** 2


class BezierCurve(list):
    def __init__(self):
        super().__init__()
        self.ellipses = []
        self.start = None
        self.end = None

    def __contains__(self, item):
        return item == self.start or item == self.end

    def draw(self, image):
        self.ellipses.clear()

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
            p1 = curve(t)
            p2 = curve(t + 0.01)
            line(image, p1, p2, (255, 0, 0), 3)
            self.ellipses.append(Ellipse((int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2)),
                                         max(abs(p1[0] - p2[0]), 4), max(abs(p1[1] - p2[1]), 4)))

    def return_other(self, point):
        if point == self.start:
            return self.end
        elif point == self.end:
            return self.start
        return None


class Curve(list):
    def __init__(self, bezier_curve: BezierCurve):
        super(Curve, self).__init__()
        self.start_point = bezier_curve[0]
        self.end_point = bezier_curve[-1]
        self.append(bezier_curve)

    def add(self, bezier_curve: BezierCurve):
        if self.start_point in bezier_curve:
            self.start_point = bezier_curve.return_other(self.start_point)
            super().insert(0, bezier_curve)
        elif self.end_point in bezier_curve:
            self.end_point = bezier_curve.return_other(self.end_point)
            super().append(bezier_curve)
        else:
            return False
        return True

    def check_merge(self, other):
        if self.start_point == other.start_point:  # pierwsze takie same - odwroc i dodaj na poczatek
            for l in other:
                self.insert(0, l)
            self.start_point = other.end_point
        elif self.end_point == other.end_point:  # ostatnie takie same - odwroc i dodaj na koniec
            other.reverse()
            self.extend(other)
            self.end_point = other.start_point
        elif self.start_point == other.end_point:  # pierwszy taki jak ostatni - dodaj na poczatek
            other.reverse()
            for l in other:
                self.insert(0, l)
            self.start_point = other.start_point
        elif self.end_point == other.start_point:  # ostatni taki jak pierwszy - dodaj na koniec
            self.extend(other)
            self.end_point = other.end_point
        else:
            return False
        return True



class Bezier(list):
    def __init__(self):
        super().__init__()

    def draw(self, image):
        for bc in self:
            bc.draw(image)

    def add_new_curve(self, buffer: Buffer):
        new = BezierCurve()
        for p in buffer:
            new.append(p)
        new.start = new[0]
        new.end = new[3]
        buffer.clear()
        if len(new) != 4:
            raise ValueError
        self.append(new)

    def delete(self, coords: tuple):
        for bc in self:
            for e in bc.ellipses:
                if coords in e:
                    self.remove(bc)
                    return True
        return False

    def find_axis(self, axis):
        max = -1
        min = 1000
        for line in self:
            for p in line:
                tmp = getattr(p, axis)
                max = tmp if tmp > max else max
                min = tmp if tmp < min else min
        return min + round((max - min) / 2)

    def output(self, sign, mode, type, do_center, do_shift, scale):
        center_x = self.find_axis('x') if do_center[0] else 0
        center_y = self.find_axis('y') if do_center[1] else 0

        def to_str_better(p):
            return p.transform(mode, type, center_x, center_y, do_shift[0], do_shift[1], scale)

        merge_lines = []
        for bc in self:
            added = False
            for ml in merge_lines:
                ml: Curve
                added = ml.add(bc)
                if added:
                    break
            if not added:
                merge_lines.append(Curve(bc))

        used_indexes = set()
        for main_index in range(len(merge_lines)):
            if main_index in used_indexes:
                continue
            for merge_index in range(0, len(merge_lines)):
                if main_index == merge_index or merge_index in used_indexes:
                    continue
                if merge_lines[main_index].check_merge(merge_lines[merge_index]):
                    used_indexes.add(merge_index)

        output = []
        for i, ml in enumerate(merge_lines):
            if i not in used_indexes:
                bezier = []
                reverse_next = False
                reverse_current = False
                for li in range(len(ml)-1):
                    if ml[li].end == ml[li+1].start:
                        reverse_current = False
                    elif ml[li].end == ml[li+1].end:
                        reverse_current = False
                        reverse_next = True
                    elif ml[li].start == ml[li+1].start:
                        reverse_current = True
                    elif ml[li].start == ml[li+1].end:
                        reverse_current = True
                        reverse_next = True
                    if reverse_current:
                        for pi,p in enumerate(ml[li][::-1]):
                            if pi or li == 0:
                                bezier.append(p)
                    else:
                        for pi, p in enumerate(ml[li]):
                            if pi or li == 0:
                                bezier.append(p)
                    if reverse_next:
                        reverse_current = True
                        reverse_next = False
                if reverse_current:
                    for pi, p in enumerate(ml[-1][::-1]):
                        if pi or len(ml) == 1:
                            bezier.append(p)
                else:
                    for pi, p in enumerate(ml[-1]):
                        if pi or len(ml) == 1:
                            bezier.append(p)
                output.append(''.join([f'POINT {sign}_{i + 1}[', str(len(bezier)), '] = {',
                                       ','.join(map(to_str_better, bezier)), '};']))
        return '\n'.join(output)
