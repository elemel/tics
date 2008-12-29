from OpenGL.GL import *
from OpenGL.GLU import *

def normalize_comp(comp):
    return float(max(0, min(comp, 1)))

def normalize_corner(corner):
    return tuple(normalize_comp(comp) for comp in corner)

class Triangle(object):
    def __init__(self, vertices):
        self.vertices = list(vertices)

    def draw(self):
        glBegin(GL_TRIANGLES)
        for vertex in self.vertices:
            glColor(vertex.r, vertex.g, vertex.b, vertex.a)
            glVertex(-1 + 2 * vertex.x, -1 + 2 * vertex.y)
        glEnd()
