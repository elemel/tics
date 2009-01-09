#include "Triangle.hpp"
#include <boost/foreach.hpp>

using boost::array;
using std::istream;
using std::ostream;

namespace tics {
    Triangle::Triangle()
    { }

    void Triangle::generate()
    {
        int r = rand() % 16, g = rand() % 16, b = rand() % 16, a = rand() % 8;
        int x = rand() % 256, y = rand() % 256;
        BOOST_FOREACH(Vertex &v, vertices_) {
            v.generate(r, g, b, a, x, y);
        }
    }

    void Triangle::draw() const
    {
        BOOST_FOREACH(const Vertex &v, vertices_) {
            v.draw();
        }
    }

    void Triangle::read(istream &in)
    {
        BOOST_FOREACH(Vertex &v, vertices_) {
            v.read(in);
        }
    }
    
    void Triangle::write(ostream &out) const
    {
        BOOST_FOREACH(const Vertex &v, vertices_) {
            v.write(out);
        }
    }
}
