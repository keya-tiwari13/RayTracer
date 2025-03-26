import math
from hittable import Hittable, Interval
from ray import Ray
from vec3 import Vec3
from material import Material
from random import random

class Camera:
    def __init__(self, aspect_ratio=1.0, image_width=100, samples_per_pixel=10, max_depth=10,
                 vfov=90, lookfrom=None, lookat=None, vup=None, defocus_angle=0, focus_dist=10):
        if lookfrom is None:
            lookfrom = Vec3(0, 0, 0)
        if lookat is None:
            lookat = Vec3(0, 0, -1)
        if vup is None:
            vup = Vec3(0, 1, 0)

        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        self.samples_per_pixel = samples_per_pixel
        self.max_depth = max_depth
        self.vfov = vfov
        self.lookfrom = lookfrom
        self.lookat = lookat
        self.vup = vup
        self.defocus_angle = defocus_angle
        self.focus_dist = focus_dist
        self.image_height = None
        self.pixel_samples_scale = None
        self.center = None
        self.pixel00_loc = None
        self.pixel_delta_u = None
        self.pixel_delta_v = None
        self.u = None
        self.v = None
        self.w = None
        self.defocus_disk_u = None
        self.defocus_disk_v = None

        self.initialize()

    def initialize(self):
        self.image_height = int(self.image_width / self.aspect_ratio)
        self.image_height = max(self.image_height, 1)
        self.pixel_samples_scale = 1.0 / self.samples_per_pixel
        self.center = self.lookfrom

        theta = math.radians(self.vfov)
        h = math.tan(theta / 2)
        viewport_height = 2 * h * self.focus_dist
        viewport_width = viewport_height * (self.image_width / self.image_height)

        self.w = (self.lookfrom - self.lookat).unit_vector()
        self.u = self.vup.cross(self.w).unit_vector()
        self.v = self.w.cross(self.u)

        viewport_u = viewport_width * self.u
        viewport_v = viewport_height * -self.v

        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        viewport_upper_left = self.center - (self.focus_dist * self.w) - viewport_u / 2 - viewport_v / 2
        self.pixel00_loc = viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)

        defocus_radius = self.focus_dist * math.tan(math.radians(self.defocus_angle / 2))
        self.defocus_disk_u = self.u * defocus_radius
        self.defocus_disk_v = self.v * defocus_radius

    def render(self, world):
        print("P3")
        print(f"{self.image_width} {self.image_height}")
        print("255")

        for j in range(self.image_height):
            print(f"\rScanlines remaining: {self.image_height - j}", end="")
            for i in range(self.image_width):
                pixel_colour = Vec3(0, 0, 0)
                for sample in range(self.samples_per_pixel):
                    r = self.get_ray(i, j)
                    pixel_colour += self.ray_colour(r, self.max_depth, world)
                self.write_colour(pixel_colour * self.pixel_samples_scale)

        print("\rDone.")

    def get_ray(self, i, j):
        offset = self.sample_square()
        pixel_sample = self.pixel00_loc + (i + offset.x()) * self.pixel_delta_u + (j + offset.y()) * self.pixel_delta_v
        ray_origin = self.center if self.defocus_angle <= 0 else self.defocus_disk_sample()
        ray_direction = pixel_sample - ray_origin
        return Ray(ray_origin, ray_direction)

    def sample_square(self):
        return Vec3(random() - 0.5, random() - 0.5, 0)

    def sample_disk(self, radius):
        return radius * self.random_in_unit_disk()

    def defocus_disk_sample(self):
        p = self.random_in_unit_disk()
        return self.center + p[0] * self.defocus_disk_u + p[1] * self.defocus_disk_v

    def ray_colour(self, r, depth, world):
        if depth <= 0:
            return Vec3(0, 0, 0)

        rec = world.hit(r, Interval(0.001, math.inf))
        if rec:
            scattered = Ray(Vec3(0, 0, 0), Vec3(0, 0, 0))
            attenuation = Vec3(0, 0, 0)
            if rec.material.scatter(r, rec, attenuation, scattered):
                return attenuation * self.ray_colour(scattered, depth - 1, world)
            return Vec3(0, 0, 0)

        unit_direction = r.direction().unit_vector()
        a = 0.5 * (unit_direction.y() + 1.0)
        return (1.0 - a) * Vec3(1.0, 1.0, 1.0) + a * Vec3(0.5, 0.7, 1.0)

    def write_colour(self, pixel_colour):
        ir = int(255.999 * pixel_colour.x())
        ig = int(255.999 * pixel_colour.y())
        ib = int(255.999 * pixel_colour.z())
        print(f"{ir} {ig} {ib}")
