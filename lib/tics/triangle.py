from OpenGL.GL import *
from OpenGL.GLU import *

def normalize_comp(comp):
    return float(max(0, min(comp, 1)))

def normalize_corner(corner):
    return tuple(normalize_comp(comp) for comp in corner)

class Triangle(object):
    def __init__(self, corners):
        self.__corners = tuple(normalize_corner(corner) for corner in corners)

    def draw(self):
        glBegin(GL_TRIANGLES)
        for r, g, b, a, x, y in self:
            glColor(r, g, b, a)
            glVertex(-1 + 2 * x, -1 + 2 * y)
        glEnd()
        
    def __iter__(self):
        return iter(self.__corners)
        
    def __hash__(self):
        return hash(self.__corners)
    
    def __eq__(self, other):
        return self.__corners == other.__corners
