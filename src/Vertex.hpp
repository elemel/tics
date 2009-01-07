#ifndef TICS_VERTEX_HPP
#define TICS_VERTEX_HPP

#include <vector>

namespace tics {
    class Vertex {
    public:
        Vertex();
        Vertex(int r, int g, int b, int a, int x, int y);
    
        void generate(int r, int g, int b, int a, int x, int y);
        void draw() const;
    
    private:
        unsigned char r_, g_, b_, a_, x_, y_;
    };
}

#endif
