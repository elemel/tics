#include "Image.hpp"
#include "Pixels.hpp"
#include "Random.hpp"
#include "Surface.hpp"
#include <cstdlib>
#include <iostream>
#include <fstream>
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
using std::cout;
using std::endl;
using std::ifstream;
using std::ios;
using std::ofstream;
using std::runtime_error;
using tics::Image;
using tics::Pixels;
using tics::Random;
using tics::Surface;

namespace {
    void init(int width, int height)
    {
        if (SDL_Init(SDL_INIT_VIDEO) != 0) {
            throw runtime_error(SDL_GetError());
        }
        atexit(SDL_Quit);

        SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, true);
        if (SDL_SetVideoMode(width, height, 32, SDL_OPENGL | SDL_SWSURFACE)
            == 0)
        {
            throw runtime_error(SDL_GetError());
        }
        
        glClearColor(0.0, 0.0, 0.0, 1.0);
        glShadeModel(GL_SMOOTH);
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    }

    void redraw(const Image &image)
    {
        glClear(GL_COLOR_BUFFER_BIT);
        image.draw();
        SDL_GL_SwapBuffers();
    }

    bool poll_quit()
    {
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT || event.type == SDL_KEYDOWN &&
                event.key.keysym.sym == SDLK_ESCAPE)
            {
                return true;
            }
        }
        return false;
    }
}

int main(int argc, char **argv)
{
    try {
        if (argc != 2) {
            throw runtime_error("missing file operand");
        }
        Random random(time(0));
        Surface goal(argv[1], 4);
        init(goal.width(), goal.height());
        Image parent(goal.width(), goal.height());
        ifstream in("image.tics", ios::binary);
        parent.read(in);
        if (!in) {
            parent.generate(256, random);
        }
        redraw(parent);
        Surface current(goal.width(), goal.height(), 32);
        current.read_display();
        double parent_f = current.fitness(goal);
        for (int g = 0; !poll_quit(); ++g) {
            Image child(parent);
            child.mutate(random);
            redraw(child);
            current.read_display();
            double child_f = current.fitness(goal);
            if (child_f < parent_f) {
                parent = child;
                parent_f = child_f;
                cout << "improved fitness to " << parent_f
                     << " in generation #" << g << endl;
            }
        }
        ofstream out("image.tics", ios::binary);
        parent.write(out);
        return 0;
    } catch (const exception &e) {
        cerr << "tics: " << e.what() << endl;
        return 1;
    }
}
