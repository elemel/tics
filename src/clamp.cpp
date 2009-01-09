#include "clamp.hpp"

using boost::uint8_t;

namespace tics {
    uint8_t clamp_uint8(int value)
    {
        if (value < 0) {
            value = 0;
        } else if (value > 255) {
            value = 255;
        }
        return uint8_t(value);
    }

    uint8_t clamp_uint4(int value)
    {
        if (value < 0) {
            value = 0;
        } else if (value > 15) {
            value = 15;
        }
        return uint8_t(value);
    }
}
