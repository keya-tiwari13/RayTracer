import math

class Interval:
    def __init__(self, min_val=math.inf, max_val=-math.inf):
        self.min = min_val
        self.max = max_val

    def size(self):
        return self.max - self.min

    def contains(self, x):
        return self.min <= x <= self.max

    def surrounds(self, x):
        return self.min < x < self.max

    def clamp(self, x):
        if x < self.min:
            return self.min
        if x > self.max:
            return self.max
        return x

    @staticmethod
    def empty():
        return Interval(math.inf, -math.inf)

    @staticmethod
    def universe():
        return Interval(-math.inf, math.inf)
