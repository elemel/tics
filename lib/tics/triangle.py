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

draw_dll = ctypes.cdll.LoadLibrary("libtics_draw.so")

TriangleBytes = ctypes.c_ubyte * 12

def clamp(min_value, value, max_value):
    value = max(min_value, value)
    value = min(value, max_value)
    return value

def clamp_byte(b):
    return clamp(0, b, 255)

def clamp_half_byte(h):
    return clamp(0, h, 15)

class Triangle(object):
    def __init__(self, bytes):
        self.__bytes = TriangleBytes()
        for i, b in enumerate(bytes):
            self.__bytes[i] = b

    def draw(self):
        draw_dll.triangle(self.__bytes)

    @classmethod
    def generate(cls):
        bytes = []
        r, g, b = [random.randrange(16) for _ in xrange(3)]
        a = random.randrange(8)
        rg = r * 16 + b
        ba = b * 16 + a
        x, y = [random.randrange(256) for _ in xrange(2)]
        d = 1 << random.randrange(8)
        for _ in xrange(3):
            bytes.append(rg)
            bytes.append(ba)
            bytes.append(x + random.choice([-1, 1]) * random.randrange(d))
            bytes.append(y + random.choice([-1, 1]) * random.randrange(d))
        return Triangle(bytes)

    @classmethod
    def read(cls, f):
        bytes = struct.unpack("!BBBBBBBBBBBB", f.read(12))
        return Triangle(bytes)

    def write(self, f):
        f.write(struct.pack("!BBBBBBBBBBBB", *self.__bytes))
            
    def mutate(self):
        mutate_func = random.choice([self.__mutate_color,
                                     self.__mutate_vertex])
        return mutate_func()
    
    def __mutate_color(self):
        bytes = list(self.__bytes)
        i = random.randrange(3) * 4
        rgba = list(divmod(bytes[i], 16) + divmod(bytes[i + 1], 16))
        d = 1 << random.randrange(4)
        j = random.randrange(4)
        rgba[j] += random.choice([-1, 1]) * random.randrange(d)
        rgba[j] = clamp_half_byte(rgba[j])
        bytes[i] = rgba[0] * 16 + rgba[1]
        bytes[i + 1] = rgba[2] * 16 + rgba[3]
        return Triangle(bytes)

    def __mutate_vertex(self):
        bytes = list(self.__bytes)
        i = random.randrange(3) * 4
        d = 1 << random.randrange(8)
        for j in xrange(i + 2, i + 4):
            bytes[j] += random.choice([-1, 1]) * random.randrange(d)
            bytes[j] = clamp_byte(bytes[j])
        return Triangle(bytes)
