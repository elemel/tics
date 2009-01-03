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

import random, struct

ATTRIBUTES = "r g b a x1 y1 x2 y2 x3 y3".split()

class Triangle(object):
    def __init__(self):
        for attr in ATTRIBUTES:
            setattr(self, attr, 0)

    def draw(self, graphics):
        graphics.draw_triangle(self.color, self.vertices)
    
    @property
    def color(self):
        return self.r / 255.0, self.g / 255.0, self.b / 255.0, self.a / 255.0

    @property
    def vertices(self):
        return ((self.x1 / 255.0, self.y1 / 255.0),
                (self.x2 / 255.0, self.y2 / 255.0),
                (self.x3 / 255.0, self.y3 / 255.0))

    @classmethod
    def generate(cls):
        triangle = Triangle()
        for attr in ATTRIBUTES:
            setattr(triangle, attr, random.randrange(256))
        return triangle

    @classmethod
    def read(cls, f):
        triangle = Triangle()
        values = struct.unpack("!BBBBBBBBBB", f.read(10))
        for attr, value in zip(ATTRIBUTES, values):
            setattr(triangle, attr, value)
        return triangle

    def write(self, f):
        values = [getattr(self, attr) for attr in ATTRIBUTES]
        f.write(struct.pack("!BBBBBBBBBB", *values))

    def mutate(self):
        attr = random.choice(ATTRIBUTES)
        setattr(self, attr, random.randrange(256))
