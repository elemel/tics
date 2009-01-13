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
from OpenGL.GL import *
from tics.triangle import Triangle

class Image(object):
    def __init__(self, (width, height), triangles):
        self.__width = width
        self.__height = height
        self.__triangles = tuple(triangles)

    def draw(self):
        glBegin(GL_TRIANGLES)
        for triangle in self.__triangles:
            triangle.draw()
        glEnd()

    @staticmethod
    def generate(resolution,  triangle_count):
        triangles = [Triangle.generate() for _ in xrange(triangle_count)]
        return Image(resolution, triangles)

    @staticmethod
    def read(f):
        width, height, triangle_count = struct.unpack("!HHH", f.read(6))
        triangles = [Triangle.read(f) for _ in xrange(triangle_count)]
        return Image((width, height), triangles)

    @staticmethod
    def load(path):
        f = open(path, "rb")
        try:
            return Image.read(f)
        finally:
            f.close()

    def write(self, f):
        f.write(struct.pack("!HHH", self.__width, self.__height,
                            len(self.__triangles)))
        for triangle in self.__triangles:
            triangle.write(f)

    def save(self, path):
        f = open(path, "wb")
        try:
            self.write(f)
        finally:
            f.close()

    def mutate(self):
        if random.random() < 0.5:
            triangles = list(self.__triangles)
            i = random.randrange(len(triangles))
            triangles[i] = triangles[i].mutate()
            return Image((self.__width, self.__height), triangles)
        else:
            mutate_func = random.choice([self.__move_triangle,
                                         self.__replace_triangle])
            return mutate_func()

    def __move_triangle(self):
        triangles = list(self.__triangles)
        i = random.randrange(len(triangles))
        j = random.randrange(len(triangles))
        triangle = triangles.pop(i)
        triangles.insert(j, triangle)
        return Image((self.__width, self.__height), triangles)

    def __replace_triangle(self):
        triangles = list(self.__triangles)
        i = random.randrange(len(triangles))
        if random.random() < 0.5:
            j = len(triangles)
        else:
            j = random.randrange(len(triangles))
        triangles.pop(i)
        triangles.insert(j, Triangle.generate())
        return Image((self.__width, self.__height), triangles)
