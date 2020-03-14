class BoundingBox:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return f'BoundingBox(x={self.x}, y={self.y}, width={self.width}, height={self.height})'

