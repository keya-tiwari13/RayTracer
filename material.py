import random
from ray import Ray
from vec3 import Vec3, dot, reflect, unit_vector, random_unit_vector, refract
from colour import colour

class Material:
    def scatter(self, r_in, rec, attenuation, scattered):
        return False


class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, r_in, rec, attenuation, scattered):
        scatter_direction = rec.normal + random_unit_vector()

        if scatter_direction.near_zero():
            scatter_direction = rec.normal

        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo
        return True


class Metal(Material):
    def __init__(self, albedo, fuzz):
        self.albedo = albedo
        self.fuzz = min(fuzz, 1) 

    def scatter(self, r_in, rec, attenuation, scattered):
        reflected = reflect(r_in.direction(), rec.normal)
        reflected = unit_vector(reflected) + (self.fuzz * random_unit_vector())
        scattered = Ray(rec.p, reflected)
        attenuation = self.albedo
        return dot(scattered.direction(), rec.normal) > 0


class Dielectric(Material):
    def __init__(self, refraction_index):
        self.refraction_index = refraction_index

    def scatter(self, r_in, rec, attenuation, scattered):
        attenuation = colour(1.0, 1.0, 1.0)
        ri = self.refraction_index if rec.front_face else (1.0 / self.refraction_index)

        unit_direction = unit_vector(r_in.direction())
        cos_theta = min(dot(-unit_direction, rec.normal), 1.0)
        sin_theta = (1.0 - cos_theta * cos_theta) ** 0.5

        cannot_refract = ri * sin_theta > 1.0
        if cannot_refract or self.reflectance(cos_theta, ri) > random.random():
            direction = reflect(unit_direction, rec.normal)
        else:
            direction = refract(unit_direction, rec.normal, ri)

        scattered = Ray(rec.p, direction)
        return True

    @staticmethod
    def reflectance(cosine, refraction_index):
        r0 = (1 - refraction_index) / (1 + refraction_index)
        r0 = r0 * r0
        return r0 + (1 - r0) * (1 - cosine) ** 5
