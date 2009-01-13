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

import sys, os, numpy, random
from pygame.locals import *
from tics.graphics import *
from tics.image import *
from tics.c_fitness import fitness

def log(message):
    sys.stderr.write("tics: %s\n" % message)

def poll_quit():
    for event in pygame.event.get():
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            return True
    return False

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        log("missing file operand")
        sys.exit(1)
    source_path = args[0]
    target_path = "%s.tics" % os.path.splitext(source_path)[0]
    pygame.init()
    try:
        source_surface = pygame.image.load(source_path).convert(32)
    except:
        log("could not load source file: %s" % source_path)
        sys.exit(1)
    resolution = source_surface.get_size()
    source_bytes = bytes_from_surface(source_surface)
    pygame.display.set_mode(resolution, OPENGL | DOUBLEBUF)
    pygame.display.set_caption("tics: %s" % os.path.basename(source_path))
    init_opengl()
    try:
        parent = Image.load(target_path)
    except:
        parent = Image.generate(resolution, 256)
    bytes = alloc_bytes(resolution)
    update_display(parent)
    bytes_from_display(resolution, bytes)
    parent_fitness = fitness(bytes, source_bytes)
    generation = 0
    log("generation = %d, fitness = %f" % (generation, parent_fitness))
    while not poll_quit():
        child = parent.mutate()
        update_display(child)
        bytes_from_display(resolution, bytes)
        child_fitness = fitness(bytes, source_bytes)
        if child_fitness < parent_fitness:
            parent = child
            parent_fitness = child_fitness
            log("generation = %d, fitness = %f" % (generation, parent_fitness))
        generation += 1
    parent.save(target_path)
    try:
        parent.save(target_path)
    except:
        log("could not save target file: %s" % target_path)
        sys.exit(1)
 
if __name__ == '__main__':
    main()
