#ifndef TICS_VERTEX_HPP
#define TICS_VERTEX_HPP

#include "Random.hpp"
#include <iostream>
#include <vector>
#include <boost/cstdint.hpp>

namespace tics {
    class Vertex {
    public:
        Vertex();
        Vertex(int red, int green, int blue, int alpha, int x, int y);
    
        void generate(int red, int green, int blue, int alpha, int x, int y,
                      Random &random);
        void mutate(Random &random);
        void draw() const;
    
        void read(std::istream &in);
        void write(std::ostream &out) const;

    private:
        boost::uint8_t red_, green_, blue_, alpha_, x_, y_;

        void mutate_color(Random &random);
        void mutate_coords(Random &random);
    };
}

#endif
