#ifndef TICS_SURFACE_HPP
#define TICS_SURFACE_HPP

#include <string>
#include <boost/noncopyable.hpp>
#include <boost/shared_ptr.hpp>
#include <SDL/SDL_video.h>

namespace tics {
    class Surface : private boost::noncopyable {
    public:
        Surface(std::size_t width, std::size_t height, std::size_t depth);
        Surface(const std::string &path, std::size_t depth);

        void flip_y();
        double fitness(Surface &other);
        double fitness(Surface &other, const SDL_Rect &rect);
        void read_display();
        void read_display(const SDL_Rect &rect);

        std::size_t width() const;
        std::size_t height() const;
        
    private:
        boost::shared_ptr<SDL_Surface> surface_;
    };
}

#endif
