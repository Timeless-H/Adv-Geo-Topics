class Point(object):
    """docstring for ."""

    def __init__(self, x, y):
        super(Point, self).__init__()
        self.x = x
        self.y = y

p = Point(3,5)
print(p.x, p.y)
