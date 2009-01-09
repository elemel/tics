#ifndef TICS_IMAGE_HPP
#define TICS_IMAGE_HPP

#include "Triangle.hpp"
#include <string>
#include <vector>

namespace tics {
    class Image {
    public:
        Image(int width, int height);

        void generate(int triangle_count);
        void mutate();
        void draw() const;
    
    private:
        unsigned short width_, height_;
        std::vector<Triangle> triangles_;
    };
}

#endif
