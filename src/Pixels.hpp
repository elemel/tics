#ifndef TICS_PIXELS_HPP
#define TICS_PIXELS_HPP

#include <string>
#include <boost/cstdint.hpp>
#include <boost/shared_array.hpp>

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
        boost::shared_array<boost::uint8_t> data_;
        int width_, height_, depth_;
        
        void resize(int width, int height, int depth);
    };
}

#endif
