#!/usr/bin/env python

# Adapted from Paul Furber's Python version of Nehe's OpenGL Lesson 3.

from __future__ import division

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame, random, sys, numpy
from pygame.locals import *
from itertools import count
from tics.generate import generate_image, generate_triangle
from tics.image import Image
from tics.mutate import mutate_image
from tics.triangle import Triangle

def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def redraw(image):
    glClear(GL_COLOR_BUFFER_BIT)
    image.draw()

def get_pixels(surface):
    width, height = surface.get_size()
    return numpy.array([[surface.get_at((x, height - y - 1))[:3]
                         for y in xrange(height)]
                        for x in xrange(width)])

def get_fitness(image_pixels, goal_pixels):
    return ((image_pixels - goal_pixels) ** 2).mean() / 255 ** 2

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
        fitness = get_fitness(image_pixels, goal_pixels)
        if fitness < best_fitness:
            print "#%d: %.7f" % (generation, fitness)
            best_image = image
            best_fitness = fitness

if __name__ == '__main__':
    main()
