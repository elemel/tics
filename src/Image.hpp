#ifndef TICS_IMAGE_HPP
#define TICS_IMAGE_HPP

#include "Random.hpp"
#include "Triangle.hpp"
#include <iostream>
#include <string>
#include <vector>
#include <boost/cstdint.hpp>

namespace tics {
    class Image {
    public:
        Image(int width, int height);

        void generate(int n, Random &random);
        void mutate(Random &random);
        void draw() const;

        void read(std::istream &in);
        void write(std::ostream &out) const;
    
    private:
        boost::uint16_t width_, height_;
        std::vector<Triangle> triangles_;

        void mutate_triangle(Random &random);
        void replace_triangle(Random &random);
        void move_triangle(Random &random);
    };
}

#endif
