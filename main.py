import sys
import math
from vec3 import Vec3, unit_vector, dot
from colour import write_colour
from ray import Ray
from rtweekend import infinity, random_double, random_double_range
from hittable_list import HittableList, HitRecord
from sphere import Sphere
from material import Lambertian, Metal, Dielectric

def ray_colour(r, world, depth):
    rec = HitRecord()
    if world.hit(r, 0.001, infinity, rec):
        scattered = Ray(Vec3(0, 0, 0), Vec3(0, 0, 0))
        attenuation = Vec3(0, 0, 0)
        if depth <= 0:
            return Vec3(0, 0, 0)
        if rec.mat.scatter(r, rec, attenuation, scattered):
            return attenuation * ray_colour(scattered, world, depth - 1)
        return Vec3(0, 0, 0)

    unit_direction = unit_vector(r.direction())
    t = 0.5 * (unit_direction.y() + 1.0)
    return (1.0 - t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)


def main():
    aspect_ratio = 16.0 / 9.0
    image_width = 400
    image_height = int(image_width / aspect_ratio)

    world = HittableList()

    ground_material = Lambertian(Vec3(0.5, 0.5, 0.5))
    world.add(Sphere(Vec3(0, -1000, 0), 1000, ground_material))

    ######### COMMENTED OUT TO TEST #########

    # for a in range(-11, 11):
    #     for b in range(-11, 11):
    #         choose_mat = random_double()
    #         center = Vec3(a + 0.9 * random_double(), 0.2, b + 0.9 * random_double())

    #         if (center - Vec3(4, 0.2, 0)).length() > 0.9:
    #             if choose_mat < 0.8:
    #                 albedo = Vec3.random() * Vec3.random()
    #                 material = Lambertian(albedo)
    #                 world.add(Sphere(center, 0.2, material))
    #             elif choose_mat < 0.95:
    #                 albedo = Vec3.random_range(0.5, 1)
    #                 fuzz = random_double_range(0, 0.5)
    #                 material = Metal(albedo, fuzz)
    #                 world.add(Sphere(center, 0.2, material))
    #             else:
    #                 material = Dielectric(1.5)
    #                 world.add(Sphere(center, 0.2, material))

    material1 = Dielectric(1.5)
    world.add(Sphere(Vec3(0, 1, 0), 1.0, material1))

    material2 = Lambertian(Vec3(0.4, 0.2, 0.1))
    world.add(Sphere(Vec3(-4, 1, 0), 1.0, material2))

    material3 = Metal(Vec3(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(Vec3(4, 1, 0), 1.0, material3))

    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * aspect_ratio
    camera_center = Vec3(13, 2, 3)

    viewport_u = Vec3(viewport_width, 0, 0)
    viewport_v = Vec3(0, -viewport_height, 0)

    pixel_delta_u = viewport_u / image_width
    pixel_delta_v = viewport_v / image_height

    viewport_upper_left = camera_center - Vec3(0, 0, focal_length) - viewport_u / 2 - viewport_v / 2
    pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)

    print(f"P3\n{image_width} {image_height}\n255")

    for j in range(image_height - 1, -1, -1):
        print(f"\rScanlines remaining: {j + 1}", end='', flush=True)
        for i in range(image_width):
            pixel_center = pixel00_loc + (i * pixel_delta_u) + (j * pixel_delta_v)
            ray_direction = pixel_center - camera_center
            r = Ray(camera_center, ray_direction)

            pixel_colour = ray_colour(r, world, 5)
            write_colour(pixel_colour)

    print("\rDone.")


if __name__ == "__main__":
    main()