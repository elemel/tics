from tics.triangle import Triangle

class Image(object):
    def __init__(self, triangles):
        self.__triangles = tuple(Triangle(t) for t in triangles)

    def draw(self):
        for triangle in self.__triangles:
            triangle.draw()
    
    def __iter__(self):
        return iter(self.__triangles)
