#ifndef TICS_PIXELS_HPP
#define TICS_PIXELS_HPP

#include <boost/shared_array.hpp>
#include <string>

namespace tics {
    class Pixels {
    public:
        Pixels();
        
        void load(const std::string &path);
        void copy_display(int width, int height);

        double fitness(const Pixels &other) const;

        int width() const;
        int height() const;
        int depth() const;
    
    private:
        boost::shared_array<unsigned char> data_;
        int width_, height_, depth_;
        
        void resize(int width, int height, int depth);
    };
}

#endif
