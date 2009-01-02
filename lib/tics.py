# Copyright (c) 2008 Mikael Lind
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame, random, sys, numpy, copy, os
from pygame.locals import *

def log(message):
    sys.stderr.write("tics: %s\n" % message)

try:
    import cPickle as pickle
except:
    log("failed to import cPickle, trying pickle instead")
    import pickle

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
    return numpy.square(pixels - goal_pixels).mean()

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
    if len(args) not in (1, 2):
        sys.stderr.write("Usage: tics <source> [<target>]\n")
        sys.exit(1)
    pygame.init()
    try:
        goal_surface = pygame.image.load(args[0])
        log("loaded source file \"%s\"" % args[0])
    except:
        log("failed to load source file \"%s\"" % args[0])
        sys.exit(1)
    width, height = size = goal_surface.get_size()
    goal_pixels = pixels_from_surface(goal_surface)
    pygame.display.set_mode(size, OPENGL | DOUBLEBUF)
    init_opengl()
    parent = [generate_triangle(random) for _ in xrange(TRIANGLE_COUNT)]
    if len(args) == 2:
        try:
            parent = pickle.load(open(args[1], "r"))
            log("loaded target file \"%s\"" % args[1])
        except:
            log("failed to load target file \"%s\"" % args[1])
            sys.exit(1)
    draw(parent)
    parent_pixels = pixels_from_display(width, height)
    parent_fitness = fitness(parent_pixels, goal_pixels)
    log("fitness is %f" % parent_fitness)
    while True:
        for event in pygame.event.get():
            if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
                if len(args) == 2:
                    pickle.dump(parent, open(args[1], "w"))
                    log("saved target file \"%s\"" % args[1])
                sys.exit(0)
        child = copy.deepcopy(parent)
        mutate(child, random)
        draw(child)
        child_pixels = pixels_from_display(width, height)
        child_fitness = fitness(child_pixels, goal_pixels)
        if child_fitness < parent_fitness:
            parent = child
            parent_pixels = child_pixels
            parent_fitness = child_fitness
            log("improved fitness to %f" % parent_fitness)

if __name__ == '__main__':
    main()
