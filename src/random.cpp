#include "random.hpp"
#include <cstdlib>

namespace tics {
    int random_sign() {
        return rand() % 2 ? -1 : 1;
    }
}
