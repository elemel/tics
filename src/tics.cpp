#include "Image.hpp"
#include <cstdlib>
#include <iostream>
#include <time.h>
#include <GL/gl.h>
#include <SDL/SDL.h>
#include <SDL/SDL_image.h>

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
}

int main(int argc, char **argv)
{
    if (argc != 2) {
        cerr << "tics: " << "missing file operand" << endl;
        return 1;
    }
    SDL_Surface *original = IMG_Load(argv[1]);
    if (original == 0) {
        cerr << "tics: " << SDL_GetError() << endl;
        return 1;
    }
    int width = original->w, height = original->h;
    if (!init_video(width, height)) {
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
