#!/usr/bin/env python

# Adapted from Paul Furber's Python version of Nehe's OpenGL Lesson 3.

from __future__ import division

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame, random, sys, numpy, copy
from pygame.locals import *
from itertools import count
from operator import itemgetter

def init_opengl():
    glShadeModel(GL_SMOOTH)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def render_individual(individual):
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_TRIANGLES)
    for triangle in sorted(individual, key=itemgetter(0)):
        for i in xrange(1, len(triangle), 6):
            x, y, r, g, b, a = triangle[i:i + 6]
            glColor(r, g, b, a)
            glVertex(-1 + 2 * x, -1 + 2 * y)
    glEnd()
    pygame.display.flip()

def get_surface_pixels(surface):
    width, height = surface.get_size()
    return numpy.array([[surface.get_at((x, height - y - 1))[:3]
                         for y in xrange(height)]
                        for x in xrange(width)])

def get_fitness(image_pixels, goal_pixels):
    return ((image_pixels - goal_pixels) ** 2).mean()

def generate_triangle(random):
    return tuple(random.random() for _ in xrange(19))

def generate_individual(triangle_count, random):
    return [generate_triangle(random) for _ in xrange(triangle_count)]

def generate_population(individual_count, triangle_count, random):
    return [generate_individual(triangle_count, random)
            for _ in xrange(individual_count)]

def crossover(mother, father, random):
    assert len(mother) == len(father)
    i = random.randrange(len(mother) + 1)
    j = random.randrange(len(mother) + 1)
    i, j = min(i, j), max(i, j)
    return mother[:i] + father[i:j] + mother[j:]

def select_parent(population, random):
    i = int(random.random() ** 2 * len(population))
    return population[i]

def mutate(child, random):
    i = random.randrange(len(child))
    triangle = list(child[i])
    j = random.randrange(len(triangle))
    triangle[j] += random.choice([-1, 1]) * random.random() ** 2
    if not (0 <= triangle[j] < 1):
        triangle[j] = random.random()
    child[i] = tuple(triangle)

def evolve_population(old_population, fitnesses, random):
    def cmp_fitness(a, b):
        return cmp(fitnesses[id(a)], fitnesses[id(b)])
    old_population.sort(cmp=cmp_fitness)
    print fitnesses[id(old_population[0])]
    new_population = [old_population[0]]
    while len(new_population) < len(old_population):
        mother = select_parent(old_population, random)
        father = select_parent(old_population, random)
        child = crossover(mother, father, random)
        mutate(child, random)
        new_population.append(child)
    return new_population

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        sys.stderr.write("Usage: tics <image>\n")
        sys.exit(1)
    pygame.init()
    goal_surface = pygame.image.load(args[0])
    width, height = size = goal_surface.get_size()
    goal_pixels = get_surface_pixels(goal_surface)
    pygame.display.set_mode(size, OPENGL | DOUBLEBUF)
    init_opengl()
    population = generate_population(64, 64, random)
    for generation in count():
        fitnesses = {}
        for event in pygame.event.get():
            if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
                break
        for individual in population:
            render_individual(individual)
            image_pixels = glReadPixels(0, 0, width, height, GL_RGB, GL_BYTE)
            fitnesses[id(individual)] = get_fitness(image_pixels, goal_pixels)
        population = evolve_population(population, fitnesses, random)

if __name__ == '__main__':
    main()
