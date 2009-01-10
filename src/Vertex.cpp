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
        : red_(0), green_(0), blue_(0), alpha_(0), x_(0), y_(0)
    { }
    
    Vertex::Vertex(int red, int green, int blue, int alpha, int x, int y)
        : red_(clamp(red, 15)),
          green_(clamp(green, 15)),
          blue_(clamp(blue, 15)),
          alpha_(clamp(alpha, 15)),
          x_(clamp(x, 255)),
          y_(clamp(y, 255))
    { }
    
    void Vertex::generate(int red, int green, int blue, int alpha,
                          int x, int y, Random &random)
    {
        red_ = clamp(red, 15);
        green_ = clamp(green, 15);
        blue_ = clamp(blue, 15);
        alpha_ = clamp(alpha, 15);
        int d = 1 << random.range(1, 8);
        x_ = clamp(x + random.offset(1, d), 255);
        y_ = clamp(y + random.offset(1, d), 255);
    }
    
    void Vertex::mutate(Random &random)
    {
        if (random.flip()) {
            int red = red_, green = green_, blue = blue_, alpha = alpha_;
            mutate_color(random);
            clog << hex << uppercase << "mutated color from "
                 << red << green << blue << alpha << " to "
                 << int(red_) << int(green_) << int(blue_) << int(alpha_)
                 << dec << endl; 
        } else {
            int x = x_, y = y_;
            mutate_coords(random);
            clog << "mutated coordinates from (" << x << ", " << y << ") to ("
                 << int(x_) << ", " << int(y_) << ")" << endl;
        }
    }
    
    void Vertex::draw() const
    {
        glColor4d(red_ / 15.0, green_ / 15.0, blue_ / 15.0, alpha_ / 15.0);
        glVertex2d(x_ / 255.0 * 2.0 - 1.0, y_ / 255.0 * 2.0 - 1.0);
    }

    void Vertex::read(istream &in)
    {
        uint8_t red_green = 0, blue_alpha = 0;
        tics::read(in, red_green);
        tics::read(in, blue_alpha);
        tics::read(in, x_);
        tics::read(in, y_);
        red_ = red_green >> 4;
        green_ = red_green & 0xf;
        blue_ = blue_alpha >> 4;
        alpha_ = blue_alpha & 0xf;
    }
    
    void Vertex::write(ostream &out) const
    {
        tics::write(out, uint8_t(red_ << 4 | green_));
        tics::write(out, uint8_t(blue_ << 4 | alpha_));
        tics::write(out, x_);
        tics::write(out, y_);
    }

    void Vertex::mutate_color(Random &random)
    {
        uint8_t *comps[4] = { &red_, &green_, &blue_, &alpha_ };
        int i = random.range(4);
        int d = 1 << random.range(1, 4);
        *comps[i] = clamp(int(*comps[i]) + random.offset(1, d), 15);
    }
    
    void Vertex::mutate_coords(Random &random)
    {
        int d = 1 << random.range(1, 8);
        x_ = clamp(int(x_) + random.offset(1, d), 255);
        y_ = clamp(int(y_) + random.offset(1, d), 255);
    }
}
