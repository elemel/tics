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

import struct

def load_triangle_image(path):
    f = open(path, "rb")
    width, height, count = struct.unpack("!HHH", f.read(6))
    image = []
    for _ in xrange(count):
        triangle = []
        for _ in xrange(3):
            x, y, r, g, b, a = struct.unpack("!HHBBBB", f.read(8))
            x /= 65535.0
            y /= 65535.0
            r /= 255.0
            g /= 255.0
            b /= 255.0
            a /= 255.0
            triangle.append([x, y, r, g, b, a])
        image.append(triangle)
    f.close()
    return image, (width, height)
    
def save_triangle_image(image, resolution, path):
    f = open(path, "wb")
    width, height = resolution
    f.write(struct.pack("!HHH", width, height, len(image)))
    for triangle in image:
        for vertex in triangle:
            x, y, r, g, b, a = vertex
            x = min(int(x * 65536), 65535)
            y = min(int(y * 65536), 65535)
            r = min(int(r * 256), 255)
            g = min(int(g * 256), 255)
            b = min(int(b * 256), 255)
            a = min(int(a * 256), 255)
            f.write(struct.pack("!HHBBBB", x, y, r, g, b, a))
    f.close()
