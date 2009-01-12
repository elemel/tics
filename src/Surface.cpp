#include "Surface.hpp"
#include <algorithm>
#include <stdexcept>
#include <boost/cstdint.hpp>
#include <boost/scoped_array.hpp>
#include <GL/gl.h>
#include <SDL/SDL_endian.h>
#include <SDL/SDL_image.h>

using boost::scoped_array;
using boost::shared_ptr;
using boost::uint8_t;
using boost::uint32_t;
using std::copy;
using std::runtime_error;
using std::size_t;
using std::string;

namespace tics {
    namespace {
        enum { big_endian = (SDL_BYTEORDER == SDL_BIG_ENDIAN) };
            
        struct ScopedLock {
            shared_ptr<SDL_Surface> surface_;
            
            explicit ScopedLock(shared_ptr<SDL_Surface> surface)
                : surface_(surface)
            {
                SDL_LockSurface(surface_.get());
            }
        
            ~ScopedLock()
            {
                SDL_UnlockSurface(surface_.get());
            }
        };

        shared_ptr<SDL_Surface> convert_rgba(shared_ptr<SDL_Surface> surface)
        {
            SDL_PixelFormat format;
            format.palette = 0;
            format.BitsPerPixel = 32;
            format.BytesPerPixel = 4;
            format.Rmask = big_endian ? 0xff000000 : 0x000000ff;
            format.Gmask = big_endian ? 0x00ff0000 : 0x0000ff00;
            format.Bmask = big_endian ? 0x0000ff00 : 0x00ff0000;
            format.Amask = big_endian ? 0x000000ff : 0xff000000;
            format.Rloss = format.Gloss = format.Bloss = format.Aloss = 0;
            format.Rshift = big_endian ? 24 : 0;
            format.Gshift = big_endian ? 16 : 8;
            format.Bshift = big_endian ? 8 : 16;
            format.Ashift = big_endian ? 0 : 24;
            format.colorkey = 0;
            format.alpha = 255;
            shared_ptr<SDL_Surface>
                surface_rgba(SDL_ConvertSurface(surface.get(), &format, 0),
                                                SDL_FreeSurface);
            if (!surface_rgba) {
                throw runtime_error(SDL_GetError());
            }
            return surface_rgba;
        }
    }

    Surface::Surface(size_t width, size_t height, size_t depth)
    {
        uint32_t red_mask = big_endian ? 0xff000000 : 0x000000ff;
        uint32_t green_mask = big_endian ? 0x00ff0000 : 0x0000ff00;
        uint32_t blue_mask = big_endian ? 0x0000ff00 : 0x00ff0000;
        uint32_t alpha_mask = big_endian ? 0x000000ff : 0xff000000;
        
        shared_ptr<SDL_Surface>
            surface(SDL_CreateRGBSurface(SDL_SWSURFACE, width, height, depth,
                                         red_mask, green_mask, blue_mask,
                                         alpha_mask),
                    SDL_FreeSurface);
        if (surface == 0) {
            throw runtime_error(SDL_GetError());
        }
        surface_ = surface;
    }

    Surface::Surface(const string &path, size_t depth)
    {
        shared_ptr<SDL_Surface> surface(IMG_Load(path.c_str()),
                                        SDL_FreeSurface);
        if (surface == 0) {
            throw runtime_error(SDL_GetError());
        }
        surface_ = convert_rgba(surface);
    }

    void Surface::flip_y()
    {
        ScopedLock lock(surface_);
        scoped_array<uint8_t> scanline(new uint8_t[surface_->pitch]);
        uint8_t *pixels = reinterpret_cast<uint8_t *>(surface_->pixels);
        size_t pitch = surface_->pitch;
        for (size_t y = 0; y != height() / 2; ++y) {
            copy(pixels + y * pitch, pixels + (y + 1) * pitch, scanline.get());
            copy(pixels + (height() - y - 1) * pitch,
                 pixels + (height() - y) * pitch, pixels + y * pitch);
            copy(scanline.get(), scanline.get() + pitch,
                 pixels + (height() - y - 1) * pitch);
        }
    }
    
    double Surface::fitness(Surface &other)
    {
        SDL_Rect rect = { 0, 0, surface_->w, surface_->h };
        return fitness(other, rect);
    }

    double Surface::fitness(Surface &other, const SDL_Rect &rect)
    {
        ScopedLock lock(surface_), other_lock(other.surface_);
        uint8_t *pixels = reinterpret_cast<uint8_t *>(surface_->pixels);
        uint8_t *other_pixels
            = reinterpret_cast<uint8_t *>(other.surface_->pixels);
        size_t pitch = surface_->pitch;
        size_t bpp = surface_->format->BytesPerPixel;
        double f = 0;
        for (size_t i = 0; i != rect.h; ++i) {
            size_t offset = (rect.y + i) * pitch + rect.x * bpp;
            uint8_t *p = pixels + offset;
            uint8_t *other_p = other_pixels + offset;
            uint8_t *last = p + rect.w * bpp;
            while (p != last) {
                int d = int(*p++) - int(*other_p++);
                f += d * d;
            }
        }
        return f;
    }

    void Surface::read_display()
    {
        ScopedLock lock(surface_);
        glFinish();
        glPixelStorei(GL_PACK_ALIGNMENT, 0);
        glReadPixels(0, 0, surface_->w, surface_->h, GL_RGBA, GL_UNSIGNED_BYTE,
                     surface_->pixels);
    }

    size_t Surface::width() const
    {
        return surface_->w;
    }
    
    size_t Surface::height() const
    {
        return surface_->h;
    }
}
