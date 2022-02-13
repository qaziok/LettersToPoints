from math import sqrt
from cv2 import circle
from geometry.conversion import *

class Point:
    def __init__(self, *args):
        if len(args) > 1:  # x,y
            self.x = args[0]
            self.y = args[1]
        else:  # tuple
            self.x = args[0][0]
            self.y = args[0][1]
        self.clicked = False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'({self.x},{self.y})'

    def transform(self,mode, type, center_x, center_y, shift_x, shift_y, scale):
        rond = 0 if type == int else 2
        new_x = round(type((self.x-center_x)*scale + shift_x), rond)
        new_y = round(type((self.y-center_y)*scale + shift_y), rond)
        if mode == 0:
            return desmos(new_x, new_y)
        if mode == 1:
            return xlib(new_x,new_y)

    def desmos(self, type, scale=1):
        if type == float:
            return f'({round(type(self.x * scale),2)},{round(type(-self.y * scale),2)})'
        return f'({type(self.x*scale)},{type(-self.y*scale)})'

    def xlib(self,scale=1):
        return f'({int(self.x*scale)},{int(self.y*scale)})'

    def rescale(self, scale):
        self.x = int(self.x * scale)
        self.y = int(self.y * scale)

    def is_near(self, coords: tuple, check_range=10):
        dist = self.distance(coords)
        if dist < check_range:
            return True
        return False

    def tuple(self):
        return (self.x, self.y)

    def distance(self, coords: tuple):
        return sqrt((self.x - coords[0]) ** 2 + (self.y - coords[1]) ** 2)

    def draw(self, image):
        point = (self.x, self.y)
        if self.clicked:
            circle(image, point, 2, (0, 0, 255), -1)
            circle(image, point, 5, (255, 0, 0))
            circle(image, point, 10, (0, 255, 255))
        else:
            circle(image, point, 2, (255, 0, 0), -1)
            circle(image, point, 5, (0, 255, 0))
            circle(image, point, 10, (255, 0, 255))

    def move(self,coords: tuple):
        self.x = coords[0]
        self.y = coords[1]
