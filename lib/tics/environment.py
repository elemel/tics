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

import pygame, ctypes, numpy
from tics.display import Display

class Environment(object):
    def __init__(self, surface, display):
        width, height = surface.get_size()
        self.__width = width
        self.__height = height
        self.__display = display
        surface = surface.convert(24)
        surface = pygame.transform.flip(surface, False, True)
        byte_count = width * height * 3
        ByteArray = ctypes.c_ubyte * byte_count
        goal = ByteArray()
        i = 0
        for y in xrange(height):
            for x in xrange(width):
                color = surface.get_at((x, y))
                for c in color[:3]:
                    goal[i] = c
                    i += 1
        self.__goal = numpy.array(goal, numpy.long)

    def fitness(self, image):
        self.__display.draw_image(image)
        pixels = self.__display.read_pixels()
        return numpy.square(numpy.subtract(pixels, self.__goal)).sum()
