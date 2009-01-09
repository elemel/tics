#include "Triangle.hpp"
#include <boost/foreach.hpp>

using boost::array;
using std::istream;
using std::ostream;

namespace tics {
    Triangle::Triangle()
    { }

    void Triangle::generate(Random &random)
    {
        int red = random.range(16), green = random.range(16),
            blue = random.range(16), alpha = random.range(8);
        int x = random.range(256), y = random.range(256);
        BOOST_FOREACH(Vertex &v, vertices_) {
            v.generate(red, green, blue, alpha, x, y, random);
        }
    }

    void Triangle::mutate(Random &random)
    {
        int i = random.range(3);
        vertices_[i].mutate(random);
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
