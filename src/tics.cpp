#include "Image.hpp"
#include <cstdlib>
#include <iostream>
#include <time.h>
#include <GL/gl.h>
#include <SDL/SDL.h>
#include <SDL/SDL_image.h>
#include <boost/shared_array.hpp>
#include <boost/shared_ptr.hpp>

using boost::shared_array;
using boost::shared_ptr;
using std::cerr;
using std::endl;
using tics::Image;

namespace {
    int init_video(int width, int height)
    {
        if (SDL_Init(SDL_INIT_VIDEO) != 0) {
            cerr << "tics: " << SDL_GetError() << endl;
            return false;
        }
        atexit(SDL_Quit);

        const SDL_VideoInfo *info = SDL_GetVideoInfo();
        if (info == 0) {
            cerr << "tics: " << SDL_GetError() << endl;
            return false;
        }

        SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, true);
        if (SDL_SetVideoMode(width, height, 32, SDL_OPENGL | SDL_SWSURFACE) ==
            0)
        {
            cerr << "tics: " << SDL_GetError() << endl;
            return false;
        }
        
        glClearColor(0.0, 0.0, 0.0, 0.0);
        glShadeModel(GL_SMOOTH);
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        return true;
    }
    
    shared_ptr<SDL_Surface> convert_surface_32(SDL_Surface &src)
    {
        SDL_PixelFormat fmt;
        fmt.palette = 0;
        fmt.BitsPerPixel = 32;
        fmt.BytesPerPixel = 4;
        fmt.Rmask = 0xff000000;
        fmt.Gmask = 0x00ff0000;
        fmt.Bmask = 0x0000ff00;
        fmt.Amask = 0x000000ff;
        fmt.Rloss =  fmt.Gloss = fmt.Bloss = fmt.Aloss = 0;
        fmt.Rshift = 24;
        fmt.Gshift = 16;
        fmt.Bshift = 8;
        fmt.Ashift = 0;
        fmt.colorkey = 0;
        fmt.alpha = 255;
        return shared_ptr<SDL_Surface>(SDL_ConvertSurface(&src, &fmt, 0),
                                       SDL_FreeSurface);
    }

    shared_array<unsigned char> copy_pixel_data(const SDL_Surface &src)
    {
        return shared_array<unsigned char>();
    }
}

int main(int argc, char **argv)
{
    if (argc != 2) {
        cerr << "tics: " << "missing file operand" << endl;
        return 1;
    }
    shared_ptr<SDL_Surface> original(IMG_Load(argv[1]), SDL_FreeSurface);
    if (original == 0) {
        cerr << "tics: " << SDL_GetError() << endl;
        return 1;
    }
    int width = original->w, height = original->h;
    if (!init_video(width, height)) {
        return 1;
    }
    shared_ptr<SDL_Surface> original_32 = convert_surface_32(*original);
    if (original_32 == 0) {
        cerr << "tics: " << SDL_GetError() << endl;
        return 1;
    }
    srand(time(0));
    Image image(width, height);
    image.generate(256);
    glClear(GL_COLOR_BUFFER_BIT);
    image.draw();
    SDL_GL_SwapBuffers();
    SDL_Delay(2500);
    return 0;
}
