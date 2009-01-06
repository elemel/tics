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

import random, struct, ctypes
from tics.config import *

draw_dll = ctypes.cdll.LoadLibrary("libtics_draw.so")

COLOR_ATTR = list("rgba")
VERTEX_ATTR = "x1 y1 x2 y2 x3 y3".split()
ATTR = COLOR_ATTR + VERTEX_ATTR

TriangleArray = ctypes.c_double * 10

class Triangle(object):
    def __init__(self, r=0, g=0, b=0, a=0, x1=0, x2=0, y1=0, y2=0, x3=0, y3=0):
        self.__r = r
        self.__g = g
        self.__b = b
        self.__a = a
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__x3 = x3
        self.__y3 = y3

        self.__array = TriangleArray()
        self.__array[0] = r / 15.0
        self.__array[1] = g / 15.0
        self.__array[2] = b / 15.0
        self.__array[3] = a / 15.0 * ALPHA_SCALE
        self.__array[4] = x1 / 255.0
        self.__array[5] = y1 / 255.0
        self.__array[6] = x2 / 255.0
        self.__array[7] = y2 / 255.0
        self.__array[8] = x3 / 255.0
        self.__array[9] = y3 / 255.0
        
    @property
    def r(self):
        return self.__r

    @property
    def g(self):
        return self.__g
        
    @property
    def b(self):
        return self.__b
        
    @property
    def a(self):
        return self.__a
    
    @property
    def x1(self):
        return self.__x1

    @property
    def y1(self):
        return self.__y1

    @property
    def x2(self):
        return self.__x2

    @property
    def y2(self):
        return self.__y2

    @property
    def x3(self):
        return self.__x3

    @property
    def y3(self):
        return self.__y3

    def draw(self):
        draw_dll.triangle(self.__array)

    @classmethod
    def generate(cls):
        kwargs = {}
        for attr in COLOR_ATTR:
            kwargs[attr] = random.randrange(16)
        for attr in VERTEX_ATTR:
            kwargs[attr] = random.randrange(256)
        return Triangle(**kwargs)

    @classmethod
    def read(cls, f):
        rg, ba = struct.unpack("!BB", f.read(2))
        r, g = divmod(rg, 16)
        b, a = divmod(ba, 16)
        x1, y1, x2, y2, x3, y3 = struct.unpack("!BBBBBB", f.read(6))
        return Triangle(r=r, g=g, b=b, a=a,
                        x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3)

    def write(self, f):
        f.write(struct.pack("!BB", self.r * 16 + self.g, self.b * 16 + self.a))
        f.write(struct.pack("!BBBBBB", self.x1, self.y1,
                            self.x2, self.y2, self.x3, self.y3))

    def mutate(self):
        mutate_func = random.choice([self.mutate_color, self.mutate_vertex])
        return mutate_func()
    
    def mutate_color(self):
        kwargs = dict((attr, getattr(self, attr)) for attr in ATTR)
        attr = random.choice(COLOR_ATTR)
        if random.random() < 0.5:
            kwargs[attr] += random.choice([-1, 1])
            kwargs[attr] = max(0, min(15, kwargs[attr]))
        else:
            kwargs[attr] = random.randrange(16)
        return Triangle(**kwargs)
        
    def mutate_vertex(self):
        kwargs = dict((attr, getattr(self, attr)) for attr in ATTR)
        attr = random.choice(VERTEX_ATTR)
        if random.random() < 0.5:
            kwargs[attr] += random.choice([-1, 1])
            kwargs[attr] = max(0, min(255, kwargs[attr]))
        else:
            kwargs[attr] = random.randrange(256)
        return Triangle(**kwargs)
