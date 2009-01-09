#include "Triangle.hpp"

using std::istream;
using std::ostream;

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

    void Triangle::read(istream &in)
    {
        v1_.read(in);
        v2_.read(in);
        v3_.read(in);
    }
    
    void Triangle::write(ostream &out) const
    {
        v1_.write(out);
        v2_.write(out);
        v3_.write(out);
    }
}
