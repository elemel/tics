#include "Pixels.hpp"
#include <iostream>
#include <stdexcept>
#include <boost/cstdint.hpp>
#include <boost/shared_ptr.hpp>
#include <SDL/SDL_image.h>
#include <GL/gl.h>

using boost::uint8_t;
using boost::shared_ptr;
using std::clog;
using std::copy;
using std::endl;
using std::logic_error;
using std::runtime_error;

namespace tics {
    namespace {
        shared_ptr<SDL_Surface> convert(SDL_Surface &src)
        {
            enum { big_endian = (SDL_BYTEORDER == SDL_BIG_ENDIAN) };
            
            SDL_PixelFormat fmt;
            fmt.palette = 0;
            fmt.BitsPerPixel = 32;
            fmt.BytesPerPixel = 4;
            fmt.Rmask = big_endian ? 0xff000000 : 0x000000ff;
            fmt.Gmask = big_endian ? 0x00ff0000 : 0x0000ff00;
            fmt.Bmask = big_endian ? 0x0000ff00 : 0x00ff0000;
            fmt.Amask = big_endian ? 0x000000ff : 0xff000000;
            fmt.Rloss = fmt.Gloss = fmt.Bloss = fmt.Aloss = 0;
            fmt.Rshift = big_endian ? 24 : 0;
            fmt.Gshift = big_endian ? 16 : 8;
            fmt.Bshift = big_endian ? 8 : 16;
            fmt.Ashift = big_endian ? 0 : 24;
            fmt.colorkey = 0;
            fmt.alpha = 255;
            shared_ptr<SDL_Surface> result(SDL_ConvertSurface(&src, &fmt, 0),
                                           SDL_FreeSurface);
            if (result == 0) {
                throw runtime_error(SDL_GetError());
            }
            return result;
        }
    }

    Pixels::Pixels()
        : width_(0), height_(0), depth_(0)
    { }
    
    void Pixels::load(const std::string &path)
    {
        shared_ptr<SDL_Surface> original(IMG_Load(path.c_str()),
                                         SDL_FreeSurface);
        if (original == 0) {
            throw runtime_error(SDL_GetError());
        }
        original = convert(*original);
        resize(original->w, original->h, 4);
        SDL_LockSurface(original.get());
        for (int y = 0; y < original->h; ++y) {
            uint8_t *first = reinterpret_cast<uint8_t *>(original->pixels) +
                             y * original->pitch;
            uint8_t *last = first + original->pitch;
            uint8_t *dest = data_.get() + (original->h - y - 1) *
                            original->pitch;
            copy(first, last, dest);
        }
        SDL_UnlockSurface(original.get());
    }
    
    void Pixels::copy_display(int width, int height)
    {
        resize(width, height, 4);
        glPixelStorei(GL_PACK_ALIGNMENT, 0);
        glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE,
                     data_.get());
    }

    double Pixels::fitness(const Pixels &other) const
    {
        if (width_ != other.width_ || height_ != other.height_ ||
            depth_ != other.depth_)
        {
            throw logic_error("pixel data must have the same dimensions");
        }
        double f = 0;
        for (int i = 0; i != width_ * height_ * depth_; ++i) {
            int d = int(data_[i]) - int(other.data_[i]);
            f += d * d;
        }
        return f / (width_ * height_ * depth_);
    }

    int Pixels::width() const { return width_; }
    int Pixels::height() const { return height_; }
    int Pixels::depth() const { return depth_; }

    void Pixels::resize(int width, int height, int depth)
    {
        if (width_ != width || height_ != height || depth_ != depth) {
            data_.reset(new unsigned char[width * height * depth]);
            width_ = width;
            height_ = height;
            depth_ = depth;
        }
    }
}
