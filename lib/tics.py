#!/usr/bin/env python

# Adapted from Paul Furber's Python version of Nehe's OpenGL Lesson 3.

from __future__ import division

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame, random, sys
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

def draw(image):
    glClear(GL_COLOR_BUFFER_BIT)
    image.draw()

def generate_triangle(random=random):
    return Triangle((random.random() for _ in xrange(6)) for _ in xrange(3))

def generate_image(triangle_count, random=random):
    return Image([generate_triangle() for _ in xrange(triangle_count)])

def get_pixels(surface):
    width, height = surface.get_size()
    return [[surface.get_at((x, height - y - 1)) for x in xrange(width)]
             for y in xrange(height)]

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        sys.stderr.write("Usage: tics <image>\n")
        sys.exit(1)
    pygame.init()
    original = pygame.image.load(args[0])
    width, height = size = original.get_size()
    original_pixels = get_pixels(original)
    pygame.display.set_mode(size, OPENGL | DOUBLEBUF)
    init()
    image = generate_image(50)
    while True:
        event = pygame.event.poll()
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            break
        draw(image)
        pygame.display.flip()
        image_pixels = glReadPixels(0, 0, width, height, GL_RGBA, GL_BYTE)

if __name__ == '__main__':
    main()
