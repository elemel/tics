#include "Image.hpp"
#include "Pixels.hpp"
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <time.h>
#include <GL/gl.h>
#include <SDL/SDL.h>
#include <SDL/SDL_image.h>
#include <boost/shared_array.hpp>
#include <boost/shared_ptr.hpp>

using boost::shared_array;
using boost::shared_ptr;
using std::exception;
using std::cerr;
using std::endl;
using std::runtime_error;
using tics::Image;
using tics::Pixels;

namespace {
    void init_sdl_gl(int width, int height)
    {
        if (SDL_Init(SDL_INIT_VIDEO) != 0) {
            throw runtime_error(SDL_GetError());
        }
        atexit(SDL_Quit);

        const SDL_VideoInfo *info = SDL_GetVideoInfo();
        if (info == 0) {
            throw runtime_error(SDL_GetError());
        }

        SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, true);
        if (SDL_SetVideoMode(width, height, 32, SDL_OPENGL | SDL_SWSURFACE) ==
            0)
        {
            throw runtime_error(SDL_GetError());
        }
        
        glClearColor(0.0, 0.0, 0.0, 0.0);
        glShadeModel(GL_SMOOTH);
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    }
}

int main(int argc, char **argv)
{
    try {
        if (argc != 2) {
            throw runtime_error("missing file operand");
        }
        Pixels original;
        original.load(argv[1]);
        init_sdl_gl(original.width(), original.height());
        Image image(original.width(), original.height());
        srand(time(0));
        for (;;) {
            image.generate(256);
            glClear(GL_COLOR_BUFFER_BIT);
            image.draw();
            SDL_GL_SwapBuffers();
        }
        return 0;
    } catch (const exception &e) {
        cerr << "tics: " << e.what() << endl;
        return 1;
    }
}
