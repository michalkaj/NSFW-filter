class BoundingBox:
    def __init__(self, x1, y1, x2, y2):
        self.upper_left = Point(x1, y1)
        self.lower_right = Point(x2, y2)

    @property
    def width(self):
        return self.lower_right.x - self.upper_left.x

    @property
    def height(self):
        return self.lower_right.y - self.upper_left.y

    @property
    def center(self):
        return Point(self.upper_left.x + self.width / 2, self.upper_left.y + self.height / 2)


class FaceBoundingBox(BoundingBox):
    def __init__(self, upper_left, lower_right, left_eye, right_eye, nose, left_mouth, right_mouth):
        super().__init__(*upper_left, *lower_right)
        self.nose = Point(*nose)
        self.left_eye = Point(*left_eye)
        self.right_eye = Point(*right_eye)
        self.left_mouth = Point(*left_mouth)
        self.right_mouth = Point(*right_mouth)


class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __repr__(self):
        return f'({self.x}, {self.y})'
