#include "Triangle.hpp"

using boost::array;
using std::istream;
using std::ostream;

namespace tics {
    Triangle::Triangle()
    { }

    void Triangle::generate()
    {
        typedef array<Vertex, 3>::iterator Iterator;
        
        int r = rand() % 16, g = rand() % 16, b = rand() % 16, a = rand() % 8;
        int x = rand() % 256, y = rand() % 256;
        for (Iterator i = vertices_.begin(); i != vertices_.end(); ++i) {
            i->generate(r, g, b, a, x, y);
        }
    }

    void Triangle::draw() const
    {
        typedef array<Vertex, 3>::const_iterator Iterator;

        for (Iterator i = vertices_.begin(); i != vertices_.end(); ++i) {
            i->draw();
        }
    }

    void Triangle::read(istream &in)
    {
        typedef array<Vertex, 3>::iterator Iterator;

        for (Iterator i = vertices_.begin(); i != vertices_.end(); ++i) {
            i->read(in);
        }
    }
    
    void Triangle::write(ostream &out) const
    {
        typedef array<Vertex, 3>::const_iterator Iterator;

        for (Iterator i = vertices_.begin(); i != vertices_.end(); ++i) {
            i->write(out);
        }
    }
}
