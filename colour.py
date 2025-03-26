from vec3 import Vec3
import sys
import math

colour = Vec3

def linear_to_gamma(linear_component):
    return math.sqrt(linear_component) if linear_component > 0 else 0

def write_colour(pixel, out_stream=sys.stdout):
    r = linear_to_gamma(pixel.x())
    g = linear_to_gamma(pixel.y())
    b = linear_to_gamma(pixel.z())
    
    r = max(0.0, min(0.999, r))
    g = max(0.0, min(0.999, g))
    b = max(0.0, min(0.999, b))
    
    rbyte = int(256 * r)
    gbyte = int(256 * g)
    bbyte = int(256 * b)
    
    out_stream.write(f"{rbyte} {gbyte} {bbyte}\n")
