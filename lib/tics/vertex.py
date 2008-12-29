def normalize_comp(comp):
    return float(max(0, min(comp, 1)))

class Vertex(object):
    def __init__(self, x, y, r, g, b, a):
        self.x, self.y = x, y
        self.r, self.g, self.b, self.a = r, g, b, a

    def __get_x(self): return self.__x
    def __get_y(self): return self.__y
    def __get_r(self): return self.__r
    def __get_g(self): return self.__g
    def __get_b(self): return self.__b
    def __get_a(self): return self.__a

    def __set_x(self, x): self.__x = normalize_comp(x)
    def __set_y(self, y): self.__y = normalize_comp(y)
    def __set_r(self, r): self.__r = normalize_comp(r)
    def __set_g(self, g): self.__g = normalize_comp(g)
    def __set_b(self, b): self.__b = normalize_comp(b)
    def __set_a(self, a): self.__a = normalize_comp(a)
    
    x = property(__get_x, __set_x)
    y = property(__get_y, __set_y)
    r = property(__get_r, __set_r)
    g = property(__get_g, __set_g)
    b = property(__get_b, __set_b)
    a = property(__get_a, __set_a)
