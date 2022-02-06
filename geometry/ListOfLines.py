from geometry.Line import Line
from geometry.Point import Point
from geometry.Curve import Curve
from cv2 import line

class ListOfLines(list):
    def __init__(self):
        super().__init__()
        self.independent_lines = []
        self.points = []

    def add(self, point1: Point, point2: Point):
        line = Line(point1,point2)
        if line not in self:
            self.append(line)

    def delete_point(self, point: Point):
        if Point is not None:
            i = 0
            while i < len(self):
                if point in self[i]:
                    self.pop(i)
                    continue
                i += 1

    def update_lines(self):
        self.independent_lines.clear()
        for line in self:
            if self.independent_lines:
                added = False
                for curve in self.independent_lines:
                    added = curve.add(line)
                    if added:
                        break
                if not added:
                    self.independent_lines.append(Curve(line))
            else:
                self.independent_lines.append(Curve(line))

        used_indexes = set()
        for main_index in range(len(self.independent_lines)):
            if main_index in used_indexes:
                continue
            for merge_index in range(0, len(self.independent_lines)):
                if main_index == merge_index or merge_index in used_indexes:
                    continue
                if self.independent_lines[main_index].check_merge(self.independent_lines[merge_index]):
                    used_indexes.add(merge_index)

        for i in range(len(self.independent_lines)):
            if i in used_indexes:
                self.independent_lines[i].clear()

    def draw(self, image):
        for line_to_draw in self:
            line(image, line_to_draw.point1.tuple(), line_to_draw.point2.tuple(), (255, 0, 0), 3)

    def generate_lines(self):
        self.update_lines()
        self.points.clear()
        i = 0
        for curve in self.independent_lines:
            if curve:
                curve.draw()
                self.points.append([])
                tmp_point = None
                for line_index in range(len(curve)-1):
                    tmp_line = curve[line_index] - curve[line_index+1]
                    self.points[i].append(tmp_line.point1)
                    tmp_point = tmp_line.point2

                if tmp_point is None:
                    tmp_point = curve[-1].point1

                self.points[i].append(curve[-1].return_other(tmp_point))
                self.points[i].append(tmp_point)
                i += 1


    def desmos(self):
        def to_str_better(p):
            return p.desmos()
        self.generate_lines()
        for point_line in self.points:
            print(','.join(map(to_str_better, point_line)))

    def xlib(self):
        def to_str_better(p):
            return p.xlib()
        self.generate_lines()
        for i,point_line in enumerate(self.points):
            print(f'XPoint test{i+1}[',len(point_line),'] = {',','.join(map(to_str_better, point_line)),'};',sep='')

    #TODO GDI - żaba
    #TODO DirectX - inicjały 3D
    #TODO OpenGL - prostokąty i ściany

    def delete(self, coords: tuple):
        for line in self:
            if line.point1.distance(coords) + line.point2.distance(coords) <= len(line) + 1:
                self.remove(line)
                return True
        return False