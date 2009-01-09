#ifndef TICS_TRIANGLE_HPP
#define TICS_TRIANGLE_HPP

#include "Vertex.hpp"
#include <iostream>

namespace tics {
    class Triangle {
    public:
        Triangle();
        
        void generate();
        void draw() const;
    
        void read(std::istream &in);
        void write(std::ostream &out) const;

    private:
        Vertex v1_, v2_, v3_;
    };
}

#endif
