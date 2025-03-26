from vec3 import Vec3, dot

class HitRecord:
    def __init__(self):
        self.p = None
        self.normal = None
        self.mat = None  
        self.t = None
        self.front_face = None

    def set_face_normal(self, r, outward_normal):
        self.front_face = dot(r.direction(), outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal

class Interval:
    def __init__(self, min_val=float('-inf'), max_val=float('inf')):
        self.min = min_val
        self.max = max_val

    def contains(self, t):
        return self.min <= t <= self.max

class Hittable:
    def hit(self, r, ray_tmin, ray_tmax, rec):
        pass
