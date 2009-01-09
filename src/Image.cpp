#include "Image.hpp"
#include "io.hpp"
#include <GL/gl.h>

using std::istream;
using std::ostream;
using std::vector;

namespace tics {
    Image::Image(int width, int height)
        : width_(width), height_(height), triangles_()
    { }
    
    void Image::generate(int n)
    {
        typedef vector<Triangle>::iterator Iterator;

        triangles_.resize(n);
        for (Iterator i = triangles_.begin(); i != triangles_.end(); ++i) {
            i->generate();
        }
    }
    
    void Image::mutate()
    {
        int i = rand() % triangles_.size();
        triangles_.erase(triangles_.begin() + i);
        triangles_.push_back(Triangle());
        triangles_.back().generate();
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

    void Image::read(istream &in)
    {
        typedef vector<Triangle>::iterator Iterator;

        uint16_t n = 0;
        tics::read(in, width_);
        tics::read(in, height_);
        tics::read(in, n);
        triangles_.resize(n);
        for (Iterator i = triangles_.begin(); i != triangles_.end(); ++i) {
            i->read(in);
        }
    }
    
    void Image::write(ostream &out) const
    {
        typedef vector<Triangle>::const_iterator Iterator;

        tics::write(out, width_);
        tics::write(out, height_);
        tics::write(out, uint16_t(triangles_.size()));
        for (Iterator i = triangles_.begin(); i != triangles_.end(); ++i) {
            i->write(out);
        }
    }
}
