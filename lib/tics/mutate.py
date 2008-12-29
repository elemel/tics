import random
from itertools import chain
from tics.generate import generate_triangle
from tics.image import Image
from tics.triangle import Triangle

def adjust(image, random=random):
    triangle = random.choice(image.triangles)
    for vertex in triangle.vertices:
        comps = [vertex.x, vertex.y, vertex.r, vertex.g, vertex.b, vertex.a]
        i = random.randrange(len(comps))
        comps[i] = random.normalvariate(comps[i], 0.1)
        vertex.x, vertex.y, vertex.r, vertex.g, vertex.b, vertex.a = comps

def replace(image, random=random):
    i = random.randrange(len(image.triangles))
    image.triangles[i] = generate_triangle(random)

def swap(image, random=random):
    triangles = image.triangles
    i = random.randrange(len(triangles))
    j = random.randrange(len(triangles))
    triangles[i], triangles[j] = triangles[j], triangles[i]

def mutate_image(image, random=random):
    mutations = [adjust, replace, swap]
    mutation = random.choice(mutations)
    mutation(image, random)
