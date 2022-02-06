from math import sqrt
from cv2 import circle


class Point:
    def __init__(self, *args):
        if len(args) > 1:  # x,y
            self.x = args[0]
            self.y = args[1]
        else:  # tuple
            self.x = args[0][0]
            self.y = args[0][1]

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'({self.x},{self.y})'

    def desmos(self):
        return f'({self.x},{600-self.y})'

    def xlib(self):
        return '{'+f'{self.x},{self.y}'+'}'

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
        circle(image, point, 2, (255, 0, 0), -1)
        circle(image, point, 5, (0, 255, 0))
        circle(image, point, 10, (255, 0, 255))

    def move(self,coords: tuple):
        self.x = coords[0]
        self.y = coords[1]
