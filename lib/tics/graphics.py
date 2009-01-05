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

from OpenGL.GL import *
import pygame, numpy, ctypes
from tics.config import *

class Graphics(object):
    def __init__(self, resolution):
        self.resolution = resolution

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT)

    def draw_triangle(self, (r, g, b, a), (x1, y1), (x2, y2), (x3, y3)):
        glBegin(GL_TRIANGLES)
        glColor4d(r, g, b, a * ALPHA_SCALE)
        glVertex2d(2.0 * x1 - 1.0, 2.0 * y1 - 1.0)
        glVertex2d(2.0 * x2 - 1.0, 2.0 * y2 - 1.0)
        glVertex2d(2.0 * x3 - 1.0, 2.0 * y3 - 1.0)
        glEnd()

    def update(self, image):
        self.clear()
        image.draw(self)
        pygame.display.flip()

def init_opengl():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def bytes_from_surface(surface):
    width, height = surface.get_size()
    bytes = []
    for y in xrange(height):
        for x in xrange(width):
            pixel = surface.get_at((x, height - y - 1))
            bytes.extend(pixel[:3])
    return numpy.array(bytes)

def bytes_from_display(resolution):
    gl = ctypes.cdll.LoadLibrary("libGL.so")
    width, height = resolution
    byte_count = width * height * 3
    ByteArray = ctypes.c_ubyte * byte_count
    bytes = ByteArray()
    gl.glPixelStorei(int(GL_PACK_ALIGNMENT), 1)
    gl.glReadPixels(0, 0, width, height, int(GL_RGB), int(GL_UNSIGNED_BYTE),
                    bytes)
    return bytes
