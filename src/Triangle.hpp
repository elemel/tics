#ifndef TICS_TRIANGLE_HPP
#define TICS_TRIANGLE_HPP

#include "Vertex.hpp"
#include <iostream>
#include <boost/array.hpp>

namespace tics {
    class Triangle {
    public:
        Triangle();
        
        void generate();
        void draw() const;
    
        void read(std::istream &in);
        void write(std::ostream &out) const;

    private:
        boost::array<Vertex, 3> vertices_;
    };
}

#endif
