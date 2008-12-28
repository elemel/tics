#!/usr/bin/env python

# Adapted from Paul Furber's Python version of Nehe's OpenGL Lesson 3.

from __future__ import division

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame, random, sys, numpy
from pygame.locals import *
from itertools import count, chain, izip

class Triangle(object):
    def __init__(self, corners):
        self.__corners = tuple(tuple(float(comp) for comp in corner)
                               for corner in corners)

    def draw(self):
        glBegin(GL_TRIANGLES)
        for r, g, b, a, x, y in self:
            glColor(r, g, b, a)
            glVertex(-1 + 2 * x, -1 + 2 * y)
        glEnd()
        
    def __iter__(self):
        return iter(self.__corners)

class Image(object):
    def __init__(self, triangles):
        self.__triangles = tuple(Triangle(t) for t in triangles)

    def draw(self):
        for triangle in self.__triangles:
            triangle.draw()
    
    def __iter__(self):
        return iter(self.__triangles)
        
    @property
    def triangles(self):
        return self.__triangles

def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def redraw(image):
    glClear(GL_COLOR_BUFFER_BIT)
    image.draw()

def generate_triangle(random=random):
    return Triangle((random.random() for _ in xrange(6)) for _ in xrange(3))

def generate_image(triangle_count, random=random):
    return Image([generate_triangle() for _ in xrange(triangle_count)])

def mutate_triangle(triangle, random=random):
    new_triangle = generate_triangle(random)
    weight = random.random()
    return Triangle(((comp * weight + new_comp * (1 - weight))
                     for comp, new_comp in izip(corner, new_corner))
                    for corner, new_corner in izip(triangle, new_triangle))

def mutate_image(image, random=random):
    triangles = image.triangles
    i = random.randrange(len(triangles))
    triangle = mutate_triangle(triangles[i], random)
    return Image(chain(triangles[:i], [triangle], triangles[i + 1:]))

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
