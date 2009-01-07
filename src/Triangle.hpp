#include "Vertex.hpp"

namespace tics {
    class Triangle {
    public:
        Triangle();
        
        void generate();
        void draw() const;
    
    private:
        Vertex v1_, v2_, v3_;
    };
}
