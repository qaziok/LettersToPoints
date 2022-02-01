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

if __name__ == '__main__':
#for c in range(ord('A'),ord('Z')+1):
    punkty = Punkty()
    letter = numpy.zeros((600, 800), dtype="uint8")
    sign = 'W'
    #cv2.putText(letter,sign,(50,480),cv2.FONT_HERSHEY_PLAIN, 40, (255, 255, 255),40)
    cv2.putText(letter, sign, (5, 590), cv2.FONT_HERSHEY_DUPLEX, 27, (255, 255, 255), 1)
    #letter = cv2.GaussianBlur(letter,(3,3),0)
    (T, letter) = cv2.threshold(letter, 200, 255, cv2.THRESH_BINARY)
    #letter = cv2.Canny(letter, 50, 240)
    #letter = cv2.resize(letter, (512, 512))
    canny = np.float32(letter)
    dst = cv2.cornerHarris(canny, 5, 3, 0.02)
    ret, dst = cv2.threshold(dst, 0.1 * dst.max(), 255, 0)
    dst = np.uint8(dst)
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(canny, np.float32(centroids), (5, 5), (-1, -1), criteria)
    rgb = cv2.cvtColor(canny, cv2.COLOR_GRAY2RGB)
    for i in range(1, len(corners)):
        #cv2.putText(rgb,str(i),(int(corners[i][0]),int(corners[i][1])),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255),2)
        punkty.add([corners[i][0],corners[i][1]])

    rgb[dst > 0.1 * dst.max()] = [0,0,255]

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 20  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 30  # minimum number of pixels making up a line
    max_line_gap = 15  # maximum gap in pixels between connectable line segments
    line_image = np.copy(rgb) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(letter, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                punkty.add([x1,y1])
                punkty.add([x2,y2])
                #cv2.line(rgb, (x1, y1), (x2, y2), (1, 0, hm), 1)
    punkty.normalize()
    punkty.scale(1)
    for i,p in enumerate(punkty):
        cv2.circle(rgb, (int(p[0]),int(p[1])), 2, (1, 0, 0), -1)
        cv2.circle(rgb, (int(p[0]),int(p[1])), 2, (1, 0, 0), -1)
        cv2.circle(rgb, (int(p[0]),int(p[1])), 5, (0, 1, 0))
        cv2.circle(rgb, (int(p[0]),int(p[1])), 5, (0, 1, 0))
        cv2.circle(rgb, (int(p[0]),int(p[1])), 10, (1, 0, 1))
        cv2.circle(rgb, (int(p[0]),int(p[1])), 10, (1, 0, 1))
        #cv2.putText(rgb,str(i),(int(p[0]),int(p[1])),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,1),1)
    cv2.imshow('image', rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#najwyżej trzeba iść po białych pixelach i pogrupować je bliskością i stosunkiem współrzędnych i z tego wyznaczyć min i max
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
