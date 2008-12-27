#!/usr/bin/env python

# Adapted from Paul Furber's Python version of Nehe's OpenGL Lesson 3.

from __future__ import division

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame, random
from pygame.locals import *

class Triangle(object):
    def __init__(self, corners):
        self.__corners = tuple(tuple(c) for c in corners)

    def draw(self):
        glBegin(GL_TRIANGLES)
        for r, g, b, a, x, y in self:
            glColor4f(r, g, b, a)
            glVertex2f(x, y)
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

def resize((width, height)):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0, 0, 0, 0)
    glClearDepth(1)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def draw(image):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(-0.5, -0.5, -1.5)
    image.draw()

def generate_triangle(random=random):
    return Triangle((random.random() for _ in xrange(6)) for _ in xrange(3))

def generate_image(triangle_count, random=random):
    return Image([generate_triangle() for _ in xrange(triangle_count)])

def main():
    resolution = 500, 500
    pygame.init()
    pygame.display.set_mode(resolution, OPENGL | DOUBLEBUF)
    resize(resolution)
    init()
    image = generate_image(50)
    while True:
        event = pygame.event.poll()
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            break
        draw(image)
        pygame.display.flip()

if __name__ == '__main__':
    main()
