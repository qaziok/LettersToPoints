class Buffer(list):
    def __init__(self, limit):
        super().__init__()
        self.limit = limit

    def full(self):
        return len(self) == self.limit

