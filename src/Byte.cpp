#include "Byte.hpp"

namespace tics {
    Byte clamp_byte(int value)
    {
        if (value < 0) {
            value = 0;
        } else if (value > 255) {
            value = 255;
        }
        return Byte(value);
    }

    Byte clamp_half_byte(int value)
    {
        if (value < 0) {
            value = 0;
        } else if (value > 15) {
            value = 15;
        }
        return Byte(value);
    }
}
