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
using std::cout;
using std::endl;
using std::runtime_error;
using tics::Image;
using tics::Pixels;

namespace {
    void init(int width, int height)
    {
        if (SDL_Init(SDL_INIT_VIDEO) != 0) {
            throw runtime_error(SDL_GetError());
        }
        atexit(SDL_Quit);

        SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, true);
        if (SDL_SetVideoMode(width, height, 32, SDL_OPENGL) == 0) {
            throw runtime_error(SDL_GetError());
        }
        
        glClearColor(0.0, 0.0, 0.0, 0.0);
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
}

int main(int argc, char **argv)
{
    try {
        if (argc != 2) {
            throw runtime_error("missing file operand");
        }
        Pixels goal;
        goal.load(argv[1]);
        init(goal.width(), goal.height());
        Image parent(goal.width(), goal.height());
        parent.generate(256);
        redraw(parent);
        Pixels current;
        current.copy_display(goal.width(), goal.height());
        double parent_f = current.fitness(goal);
        srand(time(0));
        for (int g = 0; true; ++g) {
            Image child(parent);
            child.generate(256);
            redraw(child);
            current.copy_display(goal.width(), goal.height());
            double child_f = current.fitness(goal);
            if (child_f < parent_f) {
                parent = child;
                parent_f = child_f;
                cout << "tics: generation = " << g << ", fitness = " << 
                        parent_f << endl;
            }
        }
        return 0;
    } catch (const exception &e) {
        cerr << "tics: " << e.what() << endl;
        return 1;
    }
}
