from geometry import *
import numpy as np
import cv2


class ImageProcessing:
    def __init__(self,size=(650, 800, 3)):
        self.size = size
        self.points = ListOfPoints()
        self.lines = ListOfLines()
        self.image = np.zeros(size, dtype="uint8")
        self.rgb_image = None
        self.last_drawn_image = None
        self.last_point = None

    def generate_sign(self, sign):
        cv2.putText(self.image, sign, (5, int(570*self.size[0]/650)),
                    cv2.FONT_HERSHEY_DUPLEX, int(26*self.size[0]/650), (255, 255, 255), 1)
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        corners_check = cv2.cornerHarris(gray, 5, 3, 0.02)
        ret, corners_check = cv2.threshold(corners_check, 0.1 * corners_check.max(), 255, 0)
        corners_check = np.uint8(corners_check)
        _, labels, stats, centroids = cv2.connectedComponentsWithStats(corners_check)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)
        self.rgb_image = self.image.copy()
        for i in range(1, len(corners)):
            pass
            self.points.add((round(corners[i][0]), round(corners[i][1])),check_range=10)
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
                    pass
                    p1 = self.points.add((round(x1), round(y1)))
                    p2 = self.points.add((round(x2), round(y2)))
                    #self.lines.add(p1, p2)

        self.points.normalize()

    def draw_and_update(self, image):
        self.points.draw(image)
        self.lines.draw(image)
        self.last_drawn_image = image

    def mouse_over(self, coords: tuple):
        if self.last_point:
            tmp_arrow = self.last_drawn_image.copy()
            cv2.arrowedLine(tmp_arrow, self.last_point.tuple(), coords, (127, 0, 0), 2)
            return tmp_arrow

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
        else:  # check line
            deleted_line = self.lines.delete(coords)

        self.last_point = None
        self.draw_and_update(self.rgb_image.copy())

    def loop(self):
        image_copy = self.rgb_image.copy()
        self.draw_and_update(image_copy)
        last_point = None

        def mouse_event(event, x, y, flags, param):
            image_copy = self.rgb_image.copy()
            if event == cv2.EVENT_MOUSEMOVE:
                if param and param[0]:
                    tmp_arrow = self.last_drawn_image.copy()
                    cv2.arrowedLine(tmp_arrow, param[0].tuple(), (x, y), (127, 0, 0), 2)
                    cv2.imshow('image', tmp_arrow)

            if event == cv2.EVENT_LBUTTONDOWN:
                clicked_point = self.points.check((x, y))
                if not clicked_point:
                    self.points.add((x, y))
                    self.points.normalize()
                    clicked_point = self.points.check((x, y))
                if param and param[0] and clicked_point:
                    self.lines.add(param[0], clicked_point)

                param.clear()
                param.append(clicked_point)
                self.draw_and_update(image_copy)

            if event == cv2.EVENT_RBUTTONDOWN:
                deleted_point = self.points.delete((x, y))
                if deleted_point:
                    self.lines.delete_point(deleted_point)
                else:  # check line
                    deleted_line = self.lines.delete((x, y))

                param.clear()
                self.points.normalize()
                self.draw_and_update(image_copy)

        cv2.setMouseCallback('image', mouse_event, param=[last_point])
        cv2.waitKey(0)
        self.lines.desmos()
        cv2.destroyAllWindows()