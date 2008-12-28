#!/usr/bin/env python

# Adapted from Paul Furber's Python version of Nehe's OpenGL Lesson 3.

from __future__ import division

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame, random, sys, numpy
from pygame.locals import *

class Triangle(object):
    def __init__(self, corners):
        self.__corners = tuple(tuple(c) for c in corners)

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

def get_pixels(surface):
    width, height = surface.get_size()
    return numpy.array([[surface.get_at((x, height - y - 1))
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
    while True:
        event = pygame.event.poll()
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            break
        image = generate_image(64)
        redraw(image)
        pygame.display.flip()
        image_pixels = glReadPixels(0, 0, width, height, GL_RGBA, GL_BYTE)
        fitness = ((image_pixels - goal_pixels) ** 2).mean() / 255 ** 2
        print fitness

if __name__ == '__main__':
    main()
