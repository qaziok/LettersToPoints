import numpy as np
from math import sqrt
import numpy
import cv2

class Punkty(list):
    def add(self,Punkt,waga=0):
        if len(self):
            minodl = (2000,-1)
            for i,p in enumerate(self):
                odl = sqrt((p[0] - Punkt[0]) ** 2 + (p[1] - Punkt[1]) ** 2)
                if odl < minodl[0]:
                    minodl = (odl,i)
            if minodl[0] >= 20:
                self.append(Punkt)
            elif waga:
                self[minodl[1]][0] = (self[minodl[1]][0] + Punkt[0]) / 2
                self[minodl[1]][1] = (self[minodl[1]][1] + Punkt[1]) / 2
        else:
            self.append(Punkt)

    def delete(self,Coords):
        for p in self:
            odl = sqrt((p[0] - Coords[0]) ** 2 + (p[1] - Coords[1]) ** 2)
            if odl < 10:
                self.remove(p)
                break

    def check(self,Coords):
        for p in self:
            odl = sqrt((p[0] - Coords[0]) ** 2 + (p[1] - Coords[1]) ** 2)
            if odl < 10:
                return True
        return False

    def normalize(self):
        odl = 5
        for point1 in self:
            for point2 in self:
                if point1[0] - odl < point2[0] < point1[0] + odl:
                    point2[0] = point1[0]
                if point1[1] - odl < point2[1] < point1[1] + odl:
                    point2[1] = point1[1]

    def scale(self,scale):
        for p in self:
            p[0] = scale*p[0]
            p[1] = scale*p[1]

    def draw(self,image):
        for p in self:
            pint = (int(p[0]), int(p[1]))
            cv2.circle(image, pint, 2, (1, 0, 0), -1)
            cv2.circle(image, pint, 2, (1, 0, 0), -1)
            cv2.circle(image, pint, 5, (0, 1, 0))
            cv2.circle(image, pint, 5, (0, 1, 0))
            cv2.circle(image, pint, 10, (1, 0, 1))
            cv2.circle(image, pint, 10, (1, 0, 1))

    def desmos(self):
        for p in self:
            print(f'({int(p[0])},{600-int(p[1])})',end=',')
        print()




if __name__ == '__main__':
    punkty = Punkty()
    letter = numpy.zeros((600, 800), dtype="uint8")
    sign = 'B'
    cv2.putText(letter, sign, (5, 590), cv2.FONT_HERSHEY_DUPLEX, 27, (255, 255, 255), 1)
    canny = np.float32(letter)
    dst = cv2.cornerHarris(canny, 5, 3, 0.02)
    ret, dst = cv2.threshold(dst, 0.1 * dst.max(), 255, 0)
    dst = np.uint8(dst)
    _, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(canny, np.float32(centroids), (5, 5), (-1, -1), criteria)
    rgb = cv2.cvtColor(canny, cv2.COLOR_GRAY2RGB)
    for i in range(1, len(corners)):
        punkty.add([corners[i][0],corners[i][1]])
    rgb[dst > 0.1 * dst.max()] = [0,0,255]

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 20  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 30  # minimum number of pixels making up a line
    max_line_gap = 15  # maximum gap in pixels between connectable line segments

    lines = cv2.HoughLinesP(letter, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                punkty.add([x1,y1])
                punkty.add([x2,y2])
                #cv2.line(rgb,(x1,y1),(x2,y2),(1,0,0),2)

    punkty.normalize()
    punkty.scale(1)
    #punkty.desmos()
    bbg = rgb.copy()
    punkty.draw(bbg)
    cv2.imshow('image', bbg)


    def mouse_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            bbg = rgb.copy()
            punkty.add([x,y])
            punkty.normalize()
            punkty.draw(bbg)
            cv2.imshow('image', bbg)

        if event == cv2.EVENT_RBUTTONDOWN:
            bbg = rgb.copy()
            punkty.delete([x,y])
            punkty.normalize()
            punkty.draw(bbg)
            cv2.imshow('image', bbg)

    cv2.setMouseCallback('image', mouse_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
