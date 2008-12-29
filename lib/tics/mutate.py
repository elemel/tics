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
    i = random.randrange(len(image.triangles))
    image.triangles[i] = adjust_triangle(image.triangles[i], random)

def mutate_image_replace(image, random=random):
    i = random.randrange(len(image.triangles))
    image.triangles[i] = generate_triangle(random)

def swap_items(lst, i, j):
    lst[i], lst[j] = lst[j], lst[j]

def mutate_image_swap(image, random=random):
    i = random.randrange(len(image.triangles))
    j = random.randrange(len(image.triangles))
    swap_items(image.triangles, i, j)

def mutate_image(image, random=random):
    mutations = [mutate_image_adjust, mutate_image_replace, mutate_image_swap]
    mutation = random.choice(mutations)
    mutation(image, random)
