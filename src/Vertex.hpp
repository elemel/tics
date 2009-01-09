#ifndef TICS_VERTEX_HPP
#define TICS_VERTEX_HPP

#include <iostream>
#include <vector>
#include <boost/cstdint.hpp>

namespace tics {
    class Vertex {
    public:
        Vertex();
        Vertex(int r, int g, int b, int a, int x, int y);
    
        void generate(int r, int g, int b, int a, int x, int y);
        void mutate();
        void draw() const;
    
        void read(std::istream &in);
        void write(std::ostream &out) const;

    private:
        boost::uint8_t r_, g_, b_, a_, x_, y_;

        void mutate_color();
        void mutate_coords();
    };
}

#endif
