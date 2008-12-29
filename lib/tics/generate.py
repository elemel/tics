import random
from tics.image import Image
from tics.triangle import Triangle
from tics.vertex import Vertex

def generate_vertex(random=random):
    return Vertex(*(random.random() for _ in xrange(6)))

def generate_triangle(random=random):
    return Triangle(generate_vertex() for _ in xrange(3))

def generate_image(triangle_count, random=random):
    return Image(generate_triangle(random) for _ in xrange(triangle_count))
