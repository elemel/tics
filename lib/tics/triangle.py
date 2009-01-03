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
        for vertex in triangle.vertices:
            vertex[:] = random.randrange(256), random.randrange(256)
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
        if random.random() < 0.5:
            self.color[random.randrange(4)] = random.randrange(16)
        else:
            i = random.randrange(3)
            j = random.randrange(2)
            self.vertices[i][j] = random.randrange(256)
