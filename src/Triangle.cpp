#include "Triangle.hpp"

namespace tics {
    Triangle::Triangle()
    { }

    void Triangle::generate()
    {
        int r = rand() % 16, g = rand() % 16, b = rand() % 16, a = rand() % 8;
        int x = rand() % 256, y = rand() % 256;
        v1_.generate(r, g, b, a, x, y);
        v2_.generate(r, g, b, a, x, y);
        v3_.generate(r, g, b, a, x, y);
    }

    void Triangle::draw() const
    {
        v1_.draw();
        v2_.draw();
        v3_.draw();
    }
}
