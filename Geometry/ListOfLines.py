from Geometry.Line import Line
from Geometry.Point import Point
from copy import deepcopy
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
                    if curve[0].is_connected_to(line):
                        curve.insert(0, line)
                        added = True
                        break
                    elif curve[-1].is_connected_to(line):
                        curve.append(line)
                        added = True
                        break
                if not added:
                    self.independent_lines.append([line])
            else:
                self.independent_lines.append([line])

        used_indexes = set()
        for main_index in range(len(self.independent_lines)):
            if main_index in used_indexes:
                continue
            for marge_index in range(main_index,len(self.independent_lines)):
                if main_index == marge_index or marge_index in used_indexes:
                    continue
                elif self.independent_lines[main_index][0].is_connected_to(self.independent_lines[marge_index][0]): #pierwsze takie same - odwroc i dodaj na poczatek
                    self.independent_lines[marge_index].reverse()
                    self.independent_lines[main_index] = self.independent_lines[marge_index] + self.independent_lines[main_index]
                    used_indexes.add(marge_index)
                elif self.independent_lines[main_index][-1].is_connected_to(self.independent_lines[marge_index][-1]): #ostatnie takie same - odwroc i dodaj na koniec
                    self.independent_lines[marge_index].reverse()
                    self.independent_lines[main_index] = self.independent_lines[main_index] + self.independent_lines[marge_index]
                    used_indexes.add(marge_index)
                elif self.independent_lines[main_index][0].is_connected_to(self.independent_lines[marge_index][-1]): #pierwszy taki jak ostatni - dodaj na poczatek
                    self.independent_lines[main_index] = self.independent_lines[marge_index] + self.independent_lines[main_index]
                    used_indexes.add(marge_index)
                elif self.independent_lines[main_index][-1].is_connected_to(self.independent_lines[marge_index][0]): #ostatni taki jak pierwszy - dodaj na koniec
                    self.independent_lines[main_index] = self.independent_lines[main_index] + self.independent_lines[marge_index]
                    used_indexes.add(marge_index)

        for i in range(len(self.independent_lines)):
            if i in used_indexes:
                self.independent_lines[i].clear()

    def draw(self, image):
        for l in self:
            line(image, l.point1.tuple(), l.point2.tuple(), (1, 0, 0), 3)

    def generate_lines(self):
        self.update_lines()
        self.points.clear()
        for i, curve in enumerate(self.independent_lines):
            if curve:
                self.points.append([])
                tmp_point = None
                for line_index in range(len(curve)-1):
                    tmp_line = curve[line_index] - curve[line_index+1]
                    self.points[i].append(tmp_line.point1)
                    tmp_point = tmp_line.point2
                if tmp_point:
                    tmp_line = curve[-1] - tmp_line
                    self.points[i].append(tmp_line.point1)
                    self.points[i].append(tmp_point)


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