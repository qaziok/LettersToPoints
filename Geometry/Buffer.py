from cv2 import putText, FONT_HERSHEY_SIMPLEX


class Buffer(list):
    def __init__(self, limit):
        super().__init__()
        self.limit = limit

    def full(self):
        return len(self) == self.limit

    def clear(self) -> None:
        tmp = self[-1]
        super().clear()
        self.append(tmp)

    def append(self, point):
        if not self.full():
            super(Buffer, self).append(point)

    def draw(self, image):
        for i, p in enumerate(self):
            putText(image, str(i + 1), p.tuple(), FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
