from geometry import *
import numpy as np
import cv2


# TODO lab wyjściowy do generatora - gdi musi uwzględniać kubiczne krzywe beizera,
#  opengl i directx mają mieć generowanie 3D - pewnie zaznaczanie trójkątów
#  fajnie by było poprawić błąd, że dodaje się wierzchołek ale nie bo za blisko
#  jakaś ikonka może i zrobić porządek w modułach


class ImageProcessing:
    def __init__(self, lab=0, size=(800, 700, 3)):
        self.lab = lab
        self.size = size
        self.sign = ''
        self.points = ListOfPoints()
        self.lines = ListOfLines()
        self.image = None
        self.rgb_image = None
        self.last_drawn_image = None
        # rysowanie i łączenie linii
        self.__last_point = None
        self.taken_point = None
        # rysowanie i łączenie kubicznych krzywych beziera
        self.cubic_bezier = Bezier()
        # rysowanie trójkątów
        self.triangles = ListOfTriangles()
        if lab == 2:
            self.buffer = Buffer(4)
        elif lab in (3, 4):
            self.buffer = Buffer(3)
        else:
            self.buffer = Buffer(0)

    def clear(self, lab):
        self.lab = lab
        self.sign = ''
        self.points = ListOfPoints()
        self.lines = ListOfLines()
        self.image = None
        self.rgb_image = None
        self.last_drawn_image = np.zeros(self.size, dtype="uint8")
        self.last_point = None
        self.taken_point = None
        self.cubic_bezier = Bezier()
        self.triangles = ListOfTriangles()
        if lab == 2:
            self.buffer = Buffer(4)
        elif lab in (3, 4):
            self.buffer = Buffer(3)
        else:
            self.buffer = Buffer(0)

    def generate_sign(self, sign, mode=2):
        self.sign = sign
        self.image = np.zeros(self.size, dtype="uint8")
        if mode >= 1:
            cv2.putText(self.image, sign, (5, int(570 * self.size[0] / 800)),
                        cv2.FONT_HERSHEY_DUPLEX, int(26 * self.size[0] / 800), (255, 255, 255), 1)
        self.rgb_image = self.image.copy()
        if mode in (2, 3):
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            corners_check = cv2.cornerHarris(gray, 5, 3, 0.02)
            ret, corners_check = cv2.threshold(corners_check, 0.1 * corners_check.max(), 255, 0)
            corners_check = np.uint8(corners_check)
            _, labels, stats, centroids = cv2.connectedComponentsWithStats(corners_check)
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
            corners = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)

            for i in range(1, len(corners)):
                self.points.add((round(corners[i][0]), round(corners[i][1])), check_range=18)
            self.rgb_image[corners_check > 0.1 * corners_check.max()] = [0, 0, 255]

            rho = 1  # distance resolution in pixels of the Hough grid
            theta = np.pi / 180  # angular resolution in radians of the Hough grid
            threshold = 20  # minimum number of votes (intersections in Hough grid cell)
            min_line_length = 30  # minimum number of pixels making up a line
            max_line_gap = 15  # maximum gap in pixels between connectable line segments

            lines_detection = cv2.HoughLinesP(gray, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)
            if lines_detection is not None:
                for line_check in lines_detection:
                    for x1, y1, x2, y2 in line_check:
                        p1 = self.points.add((round(x1), round(y1)))
                        p2 = self.points.add((round(x2), round(y2)))
                        if mode == 3:
                            self.lines.add(p1, p2)

        self.points.normalize()
        self.draw_and_update(self.rgb_image.copy())

    @property
    def last_point(self):
        return self.__last_point

    @last_point.setter
    def last_point(self, new):
        if self.__last_point:
            self.__last_point.clicked = False
        self.__last_point = new
        if new:
            self.__last_point.clicked = True

    def draw_and_update(self, image):
        if self.lab == 2:
            self.cubic_bezier.draw(image)
        if self.lab in (3, 4):
            self.triangles.draw(image)
        if self.lab != 2:
            self.lines.draw(image)
        self.points.draw(image)
        self.buffer.draw(image)
        self.last_drawn_image = image

    def mouse_over(self, coords: tuple):
        tmp = self.last_drawn_image.copy()
        if self.taken_point:
            self.draw_and_update(self.rgb_image.copy())
        elif self.last_point:
            cv2.arrowedLine(tmp, self.last_point.tuple(), coords, (127, 0, 0), 2)

        return tmp

    def take_point(self, coords: tuple):
        self.taken_point = self.points.check(coords)

    def move_point(self, coords: tuple):
        if self.taken_point:
            self.taken_point.move(coords)

    def point_add(self, coords: tuple):
        clicked_point = self.points.check(coords)
        if not clicked_point:
            self.points.add(coords)
            self.points.normalize()
            clicked_point = self.points.check(coords)
        if self.last_point and clicked_point:
            self.lines.add(self.last_point, clicked_point)

        self.last_point = clicked_point
        self.draw_and_update(self.rgb_image.copy())

    def point_delete(self, coords: tuple):
        deleted_point = self.points.delete(coords)
        if deleted_point:
            self.lines.delete_point(deleted_point)
            for b in self.cubic_bezier:
                if deleted_point in b:
                    self.cubic_bezier.remove(b)
        self.last_point = None
        self.draw_and_update(self.rgb_image.copy())

    def line_delete(self, coords: tuple):
        self.lines.delete(coords)
        self.cubic_bezier.delete(coords)
        self.triangles.delete(coords)
        self.draw_and_update(self.rgb_image.copy())

    def add_to_buffer(self, coords: tuple):
        point = self.points.check(coords)
        if point and point not in self.buffer:
            self.buffer.append(point)
        if self.buffer.full():
            if self.lab == 2:
                self.cubic_bezier.add_new_curve(self.buffer)
            elif self.lab in (3, 4):
                self.triangles.add_new_triangle(self.buffer)
        self.draw_and_update(self.rgb_image.copy())

    def delete_from_buffer(self, coords: tuple):
        point = self.points.check(coords)
        if point:
            try:
                self.buffer.remove(point)
            except ValueError:
                pass
        self.draw_and_update(self.rgb_image.copy())

    def output(self, type, do_center, do_shift, scale):
        output = []
        if self.lab in (0, 1, 3):
            output.append(self.lines.line_output(self.sign, self.lab, type, do_center, do_shift, scale))
        elif self.lab == 2:
            output.append(self.cubic_bezier.output(self.sign, self.lab, type, do_center, do_shift, scale))
        if self.lab == 3:
            output.append(self.triangles.output(self.points))
        return '\n'.join(output)
