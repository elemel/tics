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

import numpy, pygame
from pygame.locals import *
from OpenGL.GL import *

class Display(object):
    def __init__(self, (width, height)):
        self.__width = width
        self.__height = height
        pygame.display.set_mode((width, height),
                                OPENGL | DOUBLEBUF | SWSURFACE)
        self.caption = ""
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        glPixelStorei(GL_PACK_SKIP_PIXELS, 0)
        glPixelStorei(GL_PACK_SKIP_ROWS, 0)
        glPixelStorei(GL_PACK_SKIP_IMAGES, 0)
        glPixelStorei(GL_PACK_ROW_LENGTH, self.__width)
        glPixelStorei(GL_PACK_IMAGE_HEIGHT, self.__height)

    def __get_caption(self):
        return self.__caption

    def __set_caption(self, caption):
        self.__caption = caption
        if caption:
            pygame.display.set_caption("%s - tics" % caption)
        else:
            pygame.display.set_caption("tics")

    caption = property(__get_caption, __set_caption)

    def draw_image(self, image):
        glClear(GL_COLOR_BUFFER_BIT)
        image.draw()
        pygame.display.flip()

    def read_pixels(self):
        pixels = glReadPixelsub(0, 0, self.__width, self.__height, GL_RGB)
        return numpy.array(pixels.flat)
