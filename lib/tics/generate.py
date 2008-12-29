import random
from tics.image import Image
from tics.triangle import Triangle

def generate_triangle(random=random):
    return Triangle((random.random() for _ in xrange(6)) for _ in xrange(3))

def generate_image(triangle_count, random=random):
    return Image([generate_triangle(random) for _ in xrange(triangle_count)])
