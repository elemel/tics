#include "Vertex.hpp"
#include "clamp.hpp"
#include "io.hpp"
#include "random.hpp"
#include <GL/gl.h>

using std::clog;
using std::dec;
using std::endl;
using std::hex;
using std::istream;
using std::ostream;
using std::uppercase;

namespace tics {
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
    
    void Vertex::mutate()
    {
        if (rand() % 2) {
            int r = r_, g = g_, b = b_, a = a_;
            mutate_color();
            clog << hex << uppercase << "mutated color from "
                 << r << g << b << a << " to "
                 << int(r_) << int(g_) << int(b_) << int(a_) << dec << endl; 
        } else {
            int x = x_, y = y_;
            mutate_coords();
            clog << "mutated coordinates from (" << x << ", " << y << ") to ("
                 << int(x_) << ", " << int(y_) << ")" << endl;
        }
    }
    
    void Vertex::draw() const
    {
        glColor4d(r_ / 15.0, g_ / 15.0, b_ / 15.0, a_ / 15.0);
        glVertex2d(x_ / 255.0 * 2.0 - 1.0, y_ / 255.0 * 2.0 - 1.0);
    }

    void Vertex::read(istream &in)
    {
        uint8_t rg = 0, ba = 0;
        tics::read(in, rg);
        tics::read(in, ba);
        tics::read(in, x_);
        tics::read(in, y_);
        r_ = rg >> 4;
        g_ = rg & 0xf;
        b_ = ba >> 4;
        a_ = ba & 0xf;
    }
    
    void Vertex::write(ostream &out) const
    {
        tics::write(out, uint8_t(r_ << 4 | g_));
        tics::write(out, uint8_t(b_ << 4 | a_));
        tics::write(out, x_);
        tics::write(out, y_);
    }

    void Vertex::mutate_color()
    {
        uint8_t *comps[4] = { &r_, &g_, &b_, &a_ };
        int i = rand() % 4;
        int d = 1 << (rand() % 4);
        *comps[i] = clamp_half_byte(int(*comps[i]) +
                                   random_sign() * (rand() % d));
    }
    
    void Vertex::mutate_coords()
    {
        int d = 1 << (rand() % 8);
        x_ = clamp_byte(int(x_) + random_sign() * (rand() % d));
        y_ = clamp_byte(int(y_) + random_sign() * (rand() % d));
    }
}
