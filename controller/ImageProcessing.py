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
        self.sign = 'pusty'
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
        self.buffer = Buffer(4)
        # rysowanie trójkątów


    def generate_sign(self, sign, mode=2):
        self.sign = sign
        self.image = np.zeros(self.size, dtype="uint8")
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
            #self.buffer.append(new)
            #if self.buffer.full():
             #   self.cubic_bezier.add_new_curve(self.buffer)
              #  self.buffer.append(new)

    def draw_and_update(self, image):
        self.points.draw(image)
        self.lines.draw(image)
        #self.cubic_bezier.draw(image)
        self.last_drawn_image = image

    def mouse_over(self, coords: tuple):
        tmp = self.last_drawn_image.copy()
        if self.last_point:
            cv2.arrowedLine(tmp, self.last_point.tuple(), coords, (127, 0, 0), 2)
        elif self.taken_point:
            self.draw_and_update(self.rgb_image.copy())
            # cv2.circle(tmp, self.taken_point.tuple(),3,(0,127,0),-1)
        return tmp

    def take_point(self, coords: tuple):
        self.taken_point = self.points.check(coords)
        if self.taken_point and self.last_point:
            self.last_point = None

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

    def point_or_line_delete(self, coords: tuple):
        deleted_point = self.points.delete(coords)
        if deleted_point:
            self.lines.delete_point(deleted_point)
            for b in self.cubic_bezier:
                if deleted_point in b:
                    self.cubic_bezier.remove(b)
        else:  # check line
            deleted_line = self.lines.delete(coords)
        self.last_point = None
        self.draw_and_update(self.rgb_image.copy())

    def clear(self):
        self.points = ListOfPoints()
        self.lines = ListOfLines()
        self.image = None
        self.sign = 'pusty'
        self.rgb_image = None
        self.last_drawn_image = np.zeros(self.size, dtype="uint8")
        self.last_point = None

    def output(self, mode, type, do_center, do_shift, scale):
        return self.lines.line_output(self.sign, mode, type, do_center, do_shift, scale)
