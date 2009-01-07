#include "Vertex.hpp"
#include "clamp.hpp"
#include <GL/gl.h>

namespace tics {
    namespace {
        int random_sign() {
            return rand() % 2 ? -1 : 1;
        }
    }
    
    Vertex::Vertex()
        : r_(0), g_(0), b_(0), a_(0), x_(0), y_(0)
    { }
    
    Vertex::Vertex(int r, int g, int b, int a, int x, int y)
        : r_(clamp_half_byte(r)),
          g_(clamp_half_byte(g)),
          b_(clamp_half_byte(b)),
          a_(clamp_half_byte(a)),
          x_(clamp_byte(x)),
          y_(clamp_byte(y))
    { }
    
    void Vertex::generate(int r, int g, int b, int a, int x, int y)
    {
        r_ = clamp_half_byte(r);
        g_ = clamp_half_byte(g);
        b_ = clamp_half_byte(b);
        a_ = clamp_half_byte(a);
        int d = 1 << (rand() % 8);
        x_ = clamp_byte(x + random_sign() * (rand() % d));
        y_ = clamp_byte(y + random_sign() * (rand() % d));
    }
    
    void Vertex::draw() const
    {
        glColor4d(r_ / 15.0, g_ / 15.0, b_ / 15.0, a_ / 15.0);
        glVertex2d(x_ / 255.0 * 2.0 - 1.0, y_ / 255.0 * 2.0 - 1.0);
    }
}
