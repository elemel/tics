#include "clamp.hpp"

namespace tics {
    int clamp(int value, int max_value)
    {
        if (value < 0) {
            return 0;
        } else if (value > max_value) {
            return max_value;
        } else {
            return value;
        }
    }
}
