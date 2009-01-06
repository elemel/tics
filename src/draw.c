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

void triangle(double *data)
{
    glBegin(GL_TRIANGLES);
    glColor4d(data[0], data[1], data[2], data[3]);
    glVertex2d(2.0 * data[4] - 1.0, 2.0 * data[5] - 1.0);
    glColor4d(data[6], data[7], data[8], data[9]);
    glVertex2d(2.0 * data[10] - 1.0, 2.0 * data[11] - 1.0);
    glColor4d(data[12], data[13], data[14], data[15]);
    glVertex2d(2.0 * data[16] - 1.0, 2.0 * data[17] - 1.0);
    glEnd();
}
