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

ATTR = [c + i for i in "123" for c in "rgbaxy"]
COLOR_ATTR = [attr for attr in ATTR if attr[0] in "rgba"]
VERTEX_ATTR = [attr for attr in ATTR if attr[0] in "xy"]

TriangleData = ctypes.c_double * 18

class Triangle(object):
    def __init__(self, **kwargs):
        for attr in ATTR:
            value = kwargs.get(attr, 0)
            if attr in COLOR_ATTR:
                assert 0 <= value <= 15
            else:
                assert 0 <= value <= 255
            setattr(self, attr, value)
        self.data = TriangleData()
        for i, attr in enumerate(ATTR):
            value = kwargs.get(attr, 0)
            value /= 15.0 if attr[0] in "rgba" else 255.0
            self.data[i] = value

    def draw(self):
        draw_dll.triangle(self.data)

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
        values = []
        for _ in xrange(3):
            rg, ba = struct.unpack("!BB", f.read(2))
            values.extend(divmod(rg, 16))
            values.extend(divmod(ba, 16))
            values.extend(struct.unpack("!BB", f.read(2)))
        kwargs = dict(zip(ATTR, values))
        return Triangle(**kwargs)

    def write(self, f):
        for i in "123":
            r, g, b, a = [getattr(self, c + i) for c in "rgba"]
            f.write(struct.pack("!BB", r * 16 + g, b * 16 + a))
            x, y = [getattr(self, c + i) for c in "xy"]
            f.write(struct.pack("!BB", x, y))
            
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
