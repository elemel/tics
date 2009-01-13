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

import random
from tics.vertex import Vertex

class Triangle(object):
    def __init__(self, vertices):
        self.__vertices = tuple(vertices)

    def draw(self):
        for vertex in self.__vertices:
            vertex.draw()

    @staticmethod
    def generate():
        r, g, b = [random.randrange(16) for _ in xrange(3)]
        a = random.randrange(8)
        x, y = [random.randrange(256) for _ in xrange(2)]
        d = 1 << random.randrange(8)
        return Triangle(Vertex.generate(r, g, b, a, x, y, d)
                        for _ in xrange(3))

    @staticmethod
    def read(f):
        return Triangle(Vertex.read(f) for _ in xrange(3))

    def write(self, f):
        for vertex in self.__vertices:
            vertex.write(f)
            
    def mutate(self):
        vertices = list(self.__vertices)
        i = random.randrange(len(vertices))
        vertices[i] = vertices[i].mutate()
        return Triangle(vertices)
