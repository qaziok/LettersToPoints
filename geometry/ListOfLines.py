from geometry.Line import Line
from geometry.Point import Point
from geometry.Polyline import Polyline
from cv2 import line


class ListOfLines(list):
    def __init__(self):
        super().__init__()
        self.independent_lines = []
        self.points = []

    def add(self, point1: Point, point2: Point):
        if point1 != point2:
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
                    self.independent_lines.append(Polyline(line))
            else:
                self.independent_lines.append(Polyline(line))

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
                # curve.draw()
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

    def find_axis(self, axis):
        max = -1
        min = 1000
        for line in self.points:
            for p in line:
                tmp = getattr(p, axis)
                max = tmp if tmp > max else max
                min = tmp if tmp < min else min
        return min+round((max-min)/2)

    def line_output(self, sign, mode, type, do_center, do_shift, scale):
        self.generate_lines()
        center_x = self.find_axis('x') if do_center[0] else 0
        center_y = self.find_axis('y') if do_center[1] else 0
        def to_str_better(p):
            return p.transform(mode, type, center_x, center_y, do_shift[0], do_shift[1], scale)
        output = []
        if mode == 0:
            for point_line in self.points:
                output.append(','.join(map(to_str_better, point_line)))
        elif mode == 1:
            for i, point_line in enumerate(self.points):
                output.append(''.join([f'XPoint {sign}_{i + 1}[', str(len(point_line)), '] = {',
                                       ','.join(map(to_str_better, point_line)), '};']))
        elif mode == 3:
            for i, point_line in enumerate(self.points):
                output.append(''.join([f'SimpleVertex {sign}_{i + 1}[] =', '{',
                                       ','.join(map(to_str_better, point_line)), '};']))
                output.append(f'int {sign}_{i + 1}_amount = {len(point_line)*2};')
        return '\n'.join(output)


    #TODO GDI - żaba
    #TODO DirectX - inicjały 3D
    #TODO OpenGL - prostokąty i ściany

    def delete(self, coords: tuple):
        for line in self:
            if line.point1.distance(coords) + line.point2.distance(coords) <= len(line) + 1:
                self.remove(line)
                return True
        return False