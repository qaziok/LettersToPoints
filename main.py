import numpy as np
import numpy
import cv2

from Geometry import *

if __name__ == '__main__':
    punkty = ListOfPoints()
    linie = ListOfLines()
    letter = numpy.zeros((600, 800), dtype="uint8")
    sign = ' '
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
        punkty.add((round(corners[i][0]), round(corners[i][1])))
    rgb[dst > 0.1 * dst.max()] = [0, 0, 255]

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 20  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 30  # minimum number of pixels making up a line
    max_line_gap = 15  # maximum gap in pixels between connectable line segments

    lines = cv2.HoughLinesP(letter, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                p1 = punkty.add((round(x1), round(y1)))
                p2 = punkty.add((round(x2), round(y2)))
                #linie.add(p1, p2)

    punkty.normalize()
    punkty.scale(1)
    bbg = rgb.copy()
    punkty.draw(bbg)
    linie.draw(bbg)
    cv2.imshow('image', bbg)
    rysowanieLinii = []


    def mouse_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            bbg = rgb.copy()
            punkt = punkty.check((x, y))
            if not punkt:
                punkty.add((x, y))
                punkty.normalize()
                punkt = punkty.check((x, y))
            if param and param[0] and punkt:
                linie.add(param[0], punkt)

            param.clear()
            param.append(punkt)
            punkty.draw(bbg)
            linie.draw(bbg)
            cv2.imshow('image', bbg)

        if event == cv2.EVENT_RBUTTONDOWN:
            bbg = rgb.copy()
            deleted = punkty.delete((x, y))
            if deleted:
                linie.delete_point(deleted)
            param.clear()
            punkty.normalize()
            punkty.draw(bbg)
            linie.draw(bbg)
            cv2.imshow('image', bbg)


    cv2.setMouseCallback('image', mouse_event, param=[rysowanieLinii])
    cv2.waitKey(0)
    linie.desmos()
    #linie.xlib()

    cv2.destroyAllWindows()
