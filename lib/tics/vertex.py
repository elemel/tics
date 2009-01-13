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

import random, struct
from OpenGL.GL import *

def clamp(i, min_value, max_value):
    i = max(min_value, i)
    i = min(i, max_value)
    return i

class Vertex(object):
    def __init__(self, r=0, g=0, b=0, a=0, x=0, y=0):
        self.__r = clamp(r, 0, 15)
        self.__g = clamp(g, 0, 15)
        self.__b = clamp(b, 0, 15)
        self.__a = clamp(a, 0, 15)
        self.__x = clamp(x, 0, 255)
        self.__y = clamp(y, 0, 255)

    def draw(self):
        glColor4d(self.__r / 15.0, self.__g / 15.0, self.__b / 15.0,
                  self.__a / 15.0)
        glVertex2d(2.0 * self.__x / 255.0 - 1.0, 2.0 * self.__y / 255.0 - 1.0)
        
    @staticmethod
    def generate(r, g, b, a, x, y, d):
        return Vertex(r, g, b, a,
                      x + random.choice([-1, 1]) * random.randrange(d),
                      y + random.choice([-1, 1]) * random.randrange(d))

    @staticmethod
    def read(f):
        rg, ba, x, y = struct.unpack("!BBBB", f.read(4))
        r, g = divmod(rg, 16)
        b, a = divmod(ba, 16)
        return Vertex(r, g, b, a, x, y)

    def write(self, f):
        rg = self.__r * 16 + self.__g
        ba = self.__b * 16 + self.__a
        f.write(struct.pack("!BBBB", rg, ba, self.__x, self.__y))

    def mutate(self):
        mutate_func = random.choice([self.__mutate_color,
                                     self.__mutate_coords])
        return mutate_func()
    
    def __mutate_color(self):
        color = [self.__r, self.__g, self.__r, self.__a]
        i = random.randrange(4)
        d = 1 << random.randrange(4)
        color[i] += random.choice([-1, 1]) * random.randrange(d)
        r, g, b, a = color
        return Vertex(r, g, b, a, self.__x, self.__y)

    def __mutate_coords(self):
        coords = [self.__x, self.__y]
        d = 1 << random.randrange(8)
        for i in xrange(2):
            coords[i] += random.choice([-1, 1]) * random.randrange(d)
        x, y = coords
        return Vertex(self.__r, self.__g, self.__b, self.__a, x, y)
