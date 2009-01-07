#include "Image.hpp"
#include <GL/gl.h>

using std::vector;

namespace tics {
    Image::Image(int width, int height)
        : width_(width), height_(height), triangles_()
    { }
    
    void Image::generate(int triangle_count)
    {
        typedef vector<Triangle>::iterator Iterator;

        triangles_.resize(triangle_count);
        for (Iterator i = triangles_.begin(); i != triangles_.end(); ++i) {
            i->generate();
        }
    }

    void Image::draw() const
    {
        typedef vector<Triangle>::const_iterator Iterator;

        glBegin(GL_TRIANGLES);
        for (Iterator i = triangles_.begin(); i != triangles_.end(); ++i) {
            i->draw();
        }
        glEnd();
    }
}
