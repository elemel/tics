from tics.triangle import Triangle

class Image(object):
    def __init__(self, triangles):
        self.triangles = list(triangles)

    def draw(self):
        for triangle in self.triangles:
            triangle.draw()
