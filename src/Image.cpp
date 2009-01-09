#include "Image.hpp"
#include "io.hpp"
#include <boost/foreach.hpp>
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
        triangles_.resize(n);
        BOOST_FOREACH(Triangle &t, triangles_) {
            t.generate();
        }
    }
    
    void Image::mutate()
    {
        if (rand() % 2) {
            mutate_triangle();
        } else {
            if (rand() % 2) {
                replace_triangle();
            } else {
                move_triangle();
            }
        }
    }

    void Image::draw() const
    {
        glBegin(GL_TRIANGLES);
        BOOST_FOREACH(const Triangle &t, triangles_) {
            t.draw();
        }
        glEnd();
    }

    void Image::read(istream &in)
    {
        uint16_t n = 0;
        tics::read(in, width_);
        tics::read(in, height_);
        tics::read(in, n);
        triangles_.resize(n);
        BOOST_FOREACH(Triangle &t, triangles_) {
            t.read(in);
        }
    }
    
    void Image::write(ostream &out) const
    {
        tics::write(out, width_);
        tics::write(out, height_);
        tics::write(out, uint16_t(triangles_.size()));
        BOOST_FOREACH(const Triangle &t, triangles_) {
            t.write(out);
        }
    }

    void Image::mutate_triangle()
    {
        int i = rand() % triangles_.size();
        triangles_[i].mutate();
    }

    void Image::replace_triangle()
    {
        int i = rand() % triangles_.size();
        int j = (rand() % 2) ? rand() % triangles_.size() :
                triangles_.size() - 1;
        triangles_.erase(triangles_.begin() + i);
        triangles_.insert(triangles_.begin() + j, Triangle());
        triangles_[j].generate();
    }

    void Image::move_triangle()
    {
        int i = rand() % triangles_.size();
        int j = rand() % triangles_.size();
        Triangle t = triangles_[i];
        triangles_.erase(triangles_.begin() + i);
        triangles_.insert(triangles_.begin() + j, t);
    }
}
