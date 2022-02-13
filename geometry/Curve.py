from geometry.Line import Line


class Curve(list):
    def __init__(self, first_line: Line):
        super().__init__()
        self.start_point = first_line.point1
        self.end_point = first_line.point2
        self.append(first_line)

    def add(self, new_line: Line):
        if self.start_point in new_line:
            self.start_point = new_line.return_other(self.start_point)
            super().insert(0, new_line)
        elif self.end_point in new_line:
            self.end_point = new_line.return_other(self.end_point)
            super().append(new_line)
        else:
            return False
        return True

    def draw(self):
        first = self.start_point
        print('C:', end=' ')
        for line in self:
            print(f'({first}', end=',')
            first = line.return_other(first)
            print(f'{first})', end=',')
        print()

    def check_merge(self, other):
        if self.start_point == other.start_point:  # pierwsze takie same - odwroc i dodaj na poczatek
            for l in other:
                self.insert(0, l)
            self.start_point = other.end_point
        elif self.end_point == other.end_point:  # ostatnie takie same - odwroc i dodaj na koniec
            other.reverse()
            self.extend(other)
            self.end_point = other.start_point
        elif self.start_point == other.end_point:  # pierwszy taki jak ostatni - dodaj na poczatek
            other.reverse()
            for l in other:
                self.insert(0, l)
            self.start_point = other.start_point
        elif self.end_point == other.start_point:  # ostatni taki jak pierwszy - dodaj na koniec
            self.extend(other)
            self.end_point = other.end_point
        else:
            return False
        return True
