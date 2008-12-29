import random
from itertools import chain
from tics.generate import generate_triangle
from tics.image import Image
from tics.triangle import Triangle

def bubble(image, random=random):
    triangles = image.triangles
    i = random.randrange(len(triangles) - 1)
    triangles[i], triangles[i + 1] = triangles[i + 1], triangles[i]

def morph(image, random=random):
    triangle = random.choice(image.triangles)
    vertex = random.choice(triangle.vertices)
    setattr(vertex, random.choice("xyrgba"), random.random())
    
def replace(image, random=random):
    i = random.randrange(len(image.triangles))
    image.triangles[i] = generate_triangle(random)

def rotate(image, random=random):
    i = random.choice([-1, 1])
    image.triangles = image.triangles[i:] + image.triangles[:i]

def swap(image, random=random):
    triangles = image.triangles
    i = random.randrange(len(triangles))
    j = random.randrange(len(triangles))
    triangles[i], triangles[j] = triangles[j], triangles[i]

def mutate_image(image, random=random):
    mutations = [bubble, morph, replace, rotate, swap]
    mutation = random.choice(mutations)
    mutation(image, random)
