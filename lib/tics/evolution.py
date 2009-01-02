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

import numpy

def fitness(pixels, source_pixels):
    return numpy.square(pixels - source_pixels).mean()

def generate_triangle(random):
    triangle = []
    color = [random.random() for _ in xrange(4)]
    x = random.random()
    y = random.random()
    r = random.random() ** 3
    for _ in xrange(3):
        vertex = []
        vertex.append(clamp(x + random.choice([-1, 1]) * r *
                            random.random()))
        vertex.append(clamp(y + random.choice([-1, 1]) * r *
                            random.random()))
        vertex.extend(color)
        triangle.append(vertex)
    return triangle

def clamp(comp):
    return max(0.0, min(comp, 1.0))

def tweak_comp(comp, random):
    return clamp(comp + random.choice([-1, 1]) * random.random() ** 3)

def move_triangle(image, random):
    i = random.randrange(len(image))
    j = random.randrange(len(image))
    triangle = image.pop(i)
    image.insert(j, triangle)

def replace_triangle(image, random):
    i = random.randrange(len(image))
    j = random.randrange(len(image))
    triangle = generate_triangle(random)
    image.pop(i)
    image.insert(j, triangle)

def tweak_triangle(image, random):
    triangle = random.choice(image)
    vertex = random.choice(triangle)
    i = random.randrange(len(vertex))
    vertex[i] = tweak_comp(vertex[i], random)
    
def mutate(image, random):
    mutation = random.choice([move_triangle, replace_triangle, tweak_triangle])
    mutation(image, random)
