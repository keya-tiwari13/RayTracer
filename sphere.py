import math
from hittable import Hittable, HitRecord
from vec3 import Vec3, dot

class Sphere(Hittable):
    def __init__(self, center, radius, mat):
        self.center = center
        self.radius = max(0, radius) 
        self.mat = mat

def hit(self, r, ray_tmin, ray_tmax, rec):
    oc = r.origin() - self.center
    a = r.direction().length_squared()
    if a == 0: 
        return False

    h = dot(r.direction(), oc)
    c = oc.length_squared() - self.radius * self.radius
    discriminant = h * h - a * c

    if discriminant < 0:
        return False

    sqrtd = math.sqrt(discriminant)
    root = (h - sqrtd) / a
    if root < ray_tmin or root > ray_tmax:
        root = (h + sqrtd) / a
        if root < ray_tmin or root > ray_tmax:
            return False

    rec.t = root
    rec.p = r.at(rec.t)
    outward_normal = (rec.p - self.center) / self.radius
    rec.set_face_normal(r, outward_normal)
    rec.mat = self.mat

    return True
