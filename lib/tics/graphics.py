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

gl_dll = ctypes.cdll.LoadLibrary("libGL.so")

def init_opengl():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def update_display(image):
    glClear(GL_COLOR_BUFFER_BIT)
    image.draw()
    pygame.display.flip()

def alloc_bytes((width, height)):
    byte_count = width * height * 3
    ByteArray = ctypes.c_ubyte * byte_count
    return ByteArray()

def bytes_from_surface(surface):
    width, height = surface.get_size()
    bytes = alloc_bytes((width, height))
    i = 0
    for y in xrange(height):
        for x in xrange(width):
            color = surface.get_at((x, y))
            for c in color[:3]:
                bytes[i] = c
                i += 1
    return bytes

def bytes_from_display((width, height), bytes):
    gl_dll.glPixelStorei(int(GL_PACK_ALIGNMENT), 1)
    gl_dll.glReadPixels(0, 0, width, height, int(GL_RGB),
                        int(GL_UNSIGNED_BYTE), bytes)
