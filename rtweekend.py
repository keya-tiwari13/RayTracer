import math
import random

infinity = float('inf')
pi = 3.1415926535897932385

def degrees_to_radians(degrees):
    return degrees * pi / 180.0

def random_double():
    return random.random()

def random_double_range(min_val, max_val):
    return min_val + (max_val - min_val) * random_double()

