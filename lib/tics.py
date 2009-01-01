#!/usr/bin/env python

# Adapted from Paul Furber's Python version of Nehe's OpenGL Lesson 3.

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame, random, sys, numpy, copy
from pygame.locals import *
from itertools import count, chain
from operator import itemgetter

TRIANGLE_COUNT = 100
ALPHA_SCALE = 0.5

def init_opengl():
    glShadeModel(GL_SMOOTH)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def draw(image):
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_TRIANGLES)
    for triangle in image:
        for i in xrange(0, len(triangle), 6):
            x, y, r, g, b, a = triangle[i:i + 6]
            glColor4d(r, g, b, a * ALPHA_SCALE)
            glVertex2d(-1 + 2 * x, -1 + 2 * y)
    glEnd()
    pygame.display.flip()

def pixels_from_surface(surface):
    width, height = surface.get_size()
    return numpy.array([[surface.get_at((x, height - y - 1))[:3]
                         for x in xrange(width)] for y in xrange(height)])

def surface_from_pixels(pixels):
    width, height = len(pixels), len(pixels[0])
    surface = pygame.surface.Surface((width, height))
    for x, column in enumerate(pixels):
        for y, color in enumerate(column):
            surface.set_at((x, y), color)
    return surface
    
def fitness(pixels, goal_pixels):
    return ((pixels - goal_pixels) ** 2).mean()

def generate_triangle(random):
    triangle = []
    color = [random.random() for _ in xrange(4)]
    x = random.random()
    y = random.random()
    r = random.random() ** 3
    for _ in xrange(3):
        triangle.append(clamp(x + random.choice([-1, 1]) * r *
                              random.random()))
        triangle.append(clamp(y + random.choice([-1, 1]) * r *
                              random.random()))
        triangle.extend(color)
    return triangle

def clamp(comp):
    return max(0.0, min(comp, 1.0))

def tweak_comp(comp, random):
    return clamp(comp + random.choice([-1, 1]) * random.random() ** 3)

def move_triangle(image, random):
    i = random.randrange(len(image))
    j = random.randrange(len(image))
    triangle = image.pop(i)
    image.insert(j, triangle)

def replace_triangle(image, random):
    i = random.randrange(len(image))
    j = random.randrange(len(image))
    triangle = generate_triangle(random)
    image.pop(i)
    image.insert(j, triangle)

def tweak_triangle(image, random):
    triangle = random.choice(image)
    i = random.randrange(len(triangle))
    triangle[i] = tweak_comp(triangle[i], random)
    
def mutate(image, random):
    mutation = random.choice([move_triangle, replace_triangle, tweak_triangle])
    mutation(image, random)

def pixels_from_display(width, height):
    pixels = glReadPixelsub(0, 0, max(width, height), max(width, height),
                            GL_RGB)
    assert width >= height
    return pixels[:height]

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        sys.stderr.write("Usage: tics <image>\n")
        sys.exit(1)
    pygame.init()
    goal_surface = pygame.image.load(args[0])
    width, height = size = goal_surface.get_size()
    goal_pixels = pixels_from_surface(goal_surface)
    pygame.display.set_mode(size, OPENGL | DOUBLEBUF)
    init_opengl()
    parent = [generate_triangle(random) for _ in xrange(TRIANGLE_COUNT)]
    parent_fitness = float("inf")
    for generation in count():
        for event in pygame.event.get():
            if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
                pixels = pixels_from_display(width, height)
                pygame.image.save(surface_from_pixels(pixels), "tics.bmp")
                sys.exit(0)
        child = copy.deepcopy(parent)
        mutate(child, random)
        draw(child)
        child_pixels = pixels_from_display(width, height)
        child_fitness = fitness(child_pixels, goal_pixels)
        if child_fitness < parent_fitness:
            parent = child
            parent_fitness = child_fitness
        print ("g = %d, t = %d, f = %d"
               % (generation, pygame.time.get_ticks() / 1000.0,
                  parent_fitness))
                  
if __name__ == '__main__':
    main()
