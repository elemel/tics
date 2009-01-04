# Copyright (c) 2009 Mikael Lind
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

import random, struct, numpy
from tics.config import *

def generate_vertex_comp(comp, sigma):
    value = random.gauss(comp, sigma)
    value = int(round(value))
    if value == comp:
        value = random.choice([comp - 1, comp + 1])
    value = max(0, min(255, value))
    return value

def adjust_color_comp(comp, sigma):
    value = random.gauss(comp, sigma)
    value = int(round(value))
    if value == comp:
        value = random.choice([comp - 1, comp + 1])
    value = max(0, min(15, value))
    return value

def adjust_vertex_comp(comp, sigma):
    value = random.gauss(comp, sigma)
    value = int(round(value))
    if value == comp:
        value = random.choice([comp - 1, comp + 1])
    value = max(0, min(255, value))
    return value

class Triangle(object):
    def __init__(self):
        self.color = numpy.array([0, 0, 0, 0])
        self.vertices = numpy.array([[0, 0], [0, 0], [0, 0]])

    def draw(self, graphics):
        graphics.draw_triangle(self.color / 15.0, self.vertices / 255.0)

    @classmethod
    def generate(cls):
        triangle = Triangle()
        triangle.color[:] = [random.randrange(16) for _ in xrange(4)]
        x = random.randrange(256)
        y = random.randrange(256)
        sigma = random.choice([VERTEX_SIGMA_SMALL, VERTEX_SIGMA_MEDIUM,
                               VERTEX_SIGMA_LARGE])
        for vertex in triangle.vertices:
            vertex[:] = [generate_vertex_comp(x, sigma),
                         generate_vertex_comp(y, sigma)]
        return triangle

    @classmethod
    def read(cls, f):
        triangle = Triangle()
        rg, ba = struct.unpack("!BB", f.read(2))
        triangle.color[:] = divmod(rg, 16) + divmod(ba, 16)
        for vertex in triangle.vertices:
            vertex[:] = struct.unpack("!BB", f.read(2))
        return triangle

    def write(self, f):
        r, g, b, a = self.color
        f.write(struct.pack("!BB", r * 16 + g, b * 16 + a))
        for vertex in self.vertices:
            f.write(struct.pack("!BB", *vertex))

    def mutate(self):
        mutate_func = random.choice([self.adjust_color, self.adjust_vertex])
        mutate_func()

    def adjust_color(self):
        i = random.randrange(4)
        self.color[i] = adjust_color_comp(self.color[i], COLOR_SIGMA)

    def adjust_vertex(self):
        vertex = random.choice(self.vertices)
        i = random.randrange(2)
        sigma = random.choice([VERTEX_SIGMA_SMALL, VERTEX_SIGMA_MEDIUM,
                               VERTEX_SIGMA_LARGE])
        vertex[i] = adjust_vertex_comp(vertex[i], sigma)
