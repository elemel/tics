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
from tics.triangle import *

class Image(object):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.triangles = []

    def draw(self, graphics):
        for triangle in self.triangles:
            triangle.draw(graphics)

    @classmethod
    def generate(cls, resolution,  triangle_count):
        image = Image()
        image.resolution = resolution
        for _ in xrange(triangle_count):
            image.triangles.append(Triangle.generate())
        return image

    @classmethod
    def read(cls, f):
        image = Image()
        width, height, triangle_count = struct.unpack("!HHH", f.read(6))
        image.resolution = width, height
        for _ in xrange(triangle_count):
            image.triangles.append(Triangle.read(f))
        return image

    @classmethod        
    def load(cls, path):
        f = open(path, "rb")
        image = Image.read(f)
        f.close()
        return image

    def write(self, f):
        width, height = self.resolution
        f.write(struct.pack("!HHH", width, height, len(self.triangles)))
        for triangle in self.triangles:
            triangle.write(f)

    def save(self, path):
        f = open(path, "wb")
        self.write(f)
        f.close()

    def mutate(self):
        if random.random() < 0.5:
            triangle = random.choice(self.triangles)
            triangle.mutate()
        else:
            mutate_func = random.choice([self.mutate_move, self.mutate_replace])
            mutate_func()

    def mutate_move(self):
        i = random.randrange(len(self.triangles))
        j = random.randrange(len(self.triangles))
        triangle = self.triangles.pop(i)
        self.triangles.insert(j, triangle)

    def mutate_replace(self):
        i = random.randrange(len(self.triangles))
        self.triangles.pop(i)
        triangle = Triangle.generate()
        self.triangles.append(triangle)
