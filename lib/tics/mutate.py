import random
from itertools import chain
from tics.generate import generate_triangle
from tics.image import Image
from tics.triangle import Triangle

def adjust_triangle(triangle, random=random):
    comps = list(chain(*triangle))
    i = random.randrange(len(comps))
    comps[i] = random.normalvariate(comps[i], 0.1)
    return Triangle([comps[:6], comps[6:12], comps[12:]])

def mutate_image_adjust(image, random=random):
    triangles = list(image)
    i = random.randrange(len(triangles))
    triangles[i] = adjust_triangle(triangles[i], random)
    return Image(triangles)

def mutate_image_replace(image, random=random):
    triangles = list(image)
    i = random.randrange(len(triangles))
    triangles[i] = generate_triangle(random)
    return Image(triangles)

def mutate_image_swap(image, random=random):
    triangles = list(image)
    i = random.randrange(len(triangles))
    j = random.randrange(len(triangles))
    triangles[i], triangles[j] = triangles[j], triangles[i]
    return Image(triangles)

def mutate_image(image, random=random):
    mutations = [mutate_image_adjust, mutate_image_replace, mutate_image_swap]
    mutation = random.choice(mutations)
    return mutation(image, random)
