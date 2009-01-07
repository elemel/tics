#include "clamp.hpp"

namespace tics {
    unsigned char clamp_byte(int value)
    {
        if (value < 0) {
            value = 0;
        } else if (value > 255) {
            value = 255;
        }
        return (unsigned char)(value);
    }

    unsigned char clamp_half_byte(int value)
    {
        if (value < 0) {
            value = 0;
        } else if (value > 15) {
            value = 15;
        }
        return (unsigned char)(value);
    }
}
