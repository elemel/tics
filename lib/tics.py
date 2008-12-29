#!/usr/bin/env python

# Adapted from Paul Furber's Python version of Nehe's OpenGL Lesson 3.

from __future__ import division

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame, random, sys, numpy
from pygame.locals import *
from itertools import count, chain, izip
from tics.generate import generate_image, generate_triangle
from tics.image import Image
from tics.triangle import Triangle

def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def redraw(image):
    glClear(GL_COLOR_BUFFER_BIT)
    image.draw()

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

def get_pixels(surface):
    width, height = surface.get_size()
    return numpy.array([[surface.get_at((x, height - y - 1))[:3]
                         for y in xrange(height)]
                        for x in xrange(width)])

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        sys.stderr.write("Usage: tics <image>\n")
        sys.exit(1)
    pygame.init()
    goal_surface = pygame.image.load(args[0])
    width, height = size = goal_surface.get_size()
    goal_pixels = get_pixels(goal_surface)
    pygame.display.set_mode(size, OPENGL | DOUBLEBUF)
    init()
    best_image = generate_image(32)
    best_fitness = 1
    for generation in count():
        event = pygame.event.poll()
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            break
        image = mutate_image(best_image)
        redraw(image)
        pygame.display.flip()
        image_pixels = glReadPixels(0, 0, width, height, GL_RGB, GL_BYTE)
        fitness = ((image_pixels - goal_pixels) ** 2).mean() / 255 ** 2
        if fitness < best_fitness:
            print "#%d: %.7f" % (generation, fitness)
            best_image = image
            best_fitness = fitness

if __name__ == '__main__':
    main()
