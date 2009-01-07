/*
 * Copyright (c) 2009 Mikael Lind
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */

#include <GL/gl.h>

void draw_triangle(unsigned char *bytes)
{
    int i;
    unsigned char r, g, b, a;
    double x, y;

    glBegin(GL_TRIANGLES);
    for (i = 0; i != 12; i += 4) {
        r = bytes[i] / 16;
        g = bytes[i] % 16;
        b = bytes[i + 1] / 16;
        a = bytes[i + 1] % 16;
        x = bytes[i + 2] / 255.0;
        y = bytes[i + 3] / 255.0;
        glColor4ub(r * 17, g * 17, b * 17, a * 17);
        glVertex2d(2.0 * x - 1.0, 2.0 * y - 1.0);
    }
    glEnd();
}
