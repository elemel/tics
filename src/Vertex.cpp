#include "Vertex.hpp"
#include "clamp.hpp"
#include "io.hpp"
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
        : r_(clamp_uint4(r)),
          g_(clamp_uint4(g)),
          b_(clamp_uint4(b)),
          a_(clamp_uint4(a)),
          x_(clamp_uint8(x)),
          y_(clamp_uint8(y))
    { }
    
    void Vertex::generate(int r, int g, int b, int a, int x, int y,
                          Random &random)
    {
        r_ = clamp_uint4(r);
        g_ = clamp_uint4(g);
        b_ = clamp_uint4(b);
        a_ = clamp_uint4(a);
        int d = 1 << random.range(1, 8);
        x_ = clamp_uint8(x + random.offset(1, d));
        y_ = clamp_uint8(y + random.offset(1, d));
    }
    
    void Vertex::mutate(Random &random)
    {
        if (random.flip()) {
            int r = r_, g = g_, b = b_, a = a_;
            mutate_color(random);
            clog << hex << uppercase << "mutated color from "
                 << r << g << b << a << " to "
                 << int(r_) << int(g_) << int(b_) << int(a_) << dec << endl; 
        } else {
            int x = x_, y = y_;
            mutate_coords(random);
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

    void Vertex::mutate_color(Random &random)
    {
        uint8_t *comps[4] = { &r_, &g_, &b_, &a_ };
        int i = random.range(4);
        int d = 1 << random.range(1, 4);
        *comps[i] = clamp_uint4(int(*comps[i]) + random.offset(1, d));
    }
    
    void Vertex::mutate_coords(Random &random)
    {
        int d = 1 << random.range(1, 8);
        x_ = clamp_uint8(int(x_) + random.offset(1, d));
        y_ = clamp_uint8(int(y_) + random.offset(1, d));
    }
}
