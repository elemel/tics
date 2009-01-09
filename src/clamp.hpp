#ifndef TICS_CLAMP_HPP
#define TICS_CLAMP_HPP

#include <boost/cstdint.hpp>

namespace tics {
    boost::uint8_t clamp_byte(int value);
    boost::uint8_t clamp_half_byte(int value);
}

#endif
