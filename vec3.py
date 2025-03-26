import math
import random

class Vec3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.e = [x, y, z]

    def x(self):
        return self.e[0]
    
    def y(self):
        return self.e[1]
    
    def z(self):
        return self.e[2]
    
    def __neg__(self):
        return Vec3(-self.e[0], -self.e[1], -self.e[2])
    
    def __getitem__(self, i):
        return self.e[i]
    
    def __setitem__(self, i, value):
        self.e[i] = value
    
    def __iadd__(self, v):
        self.e[0] += v.e[0]
        self.e[1] += v.e[1]
        self.e[2] += v.e[2]
        return self
    
    def __isub__(self, v):
        self.e[0] -= v.e[0]
        self.e[1] -= v.e[1]
        self.e[2] -= v.e[2]
        return self
    
    def __imul__(self, t):
        self.e[0] *= t
        self.e[1] *= t
        self.e[2] *= t
        return self
    
    def __itruediv__(self, t):
        return self.__imul__(1 / t)
    
    def __add__(self, other):
        return Vec3(self.e[0] + other.e[0], self.e[1] + other.e[1], self.e[2] + other.e[2])
    
    def __sub__(self, other):
        return Vec3(self.e[0] - other.e[0], self.e[1] - other.e[1], self.e[2] - other.e[2])
    
    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.e[0] * other.e[0], self.e[1] * other.e[1], self.e[2] * other.e[2])
        return Vec3(self.e[0] * other, self.e[1] * other, self.e[2] * other)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, t):
        return Vec3(self.e[0] / t, self.e[1] / t, self.e[2] / t)
    
    def length(self):
        return math.sqrt(self.length_squared())
    
    def length_squared(self):
        return self.e[0] ** 2 + self.e[1] ** 2 + self.e[2] ** 2
    
    def near_zero(self):
        s = 1e-8
        return abs(self.e[0]) < s and abs(self.e[1]) < s and abs(self.e[2]) < s
    
    @staticmethod
    def random():
        return Vec3(random.random(), random.random(), random.random())
    
    @staticmethod
    def random_range(min_val, max_val):
        return Vec3(random.uniform(min_val, max_val), random.uniform(min_val, max_val), random.uniform(min_val, max_val))

def dot(u, v):
    return u.e[0] * v.e[0] + u.e[1] * v.e[1] + u.e[2] * v.e[2]

def cross(u, v):
    return Vec3(
        u.e[1] * v.e[2] - u.e[2] * v.e[1],
        u.e[2] * v.e[0] - u.e[0] * v.e[2],
        u.e[0] * v.e[1] - u.e[1] * v.e[0]
    )

def unit_vector(v):
    return v / v.length()

def random_in_unit_disk():
    while True:
        p = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), 0)
        if p.length_squared() < 1:
            return p

def random_unit_vector():
    while True:
        p = Vec3.random_range(-1, 1)
        lensq = p.length_squared()
        if 1e-160 < lensq <= 1.0:
            return p / math.sqrt(lensq)

def random_on_hemisphere(normal):
    on_unit_sphere = random_unit_vector()
    return on_unit_sphere if dot(on_unit_sphere, normal) > 0.0 else -on_unit_sphere

def reflect(v, n):
    return v - 2 * dot(v, n) * n

def refract(uv, n, etai_over_etat):
    cos_theta = min(dot(-uv, n), 1.0)
    r_out_perp = etai_over_etat * (uv + cos_theta * n)
    r_out_parallel = -math.sqrt(abs(1.0 - r_out_perp.length_squared())) * n
    return r_out_perp + r_out_parallel
