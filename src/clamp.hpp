#ifndef TICS_CLAMP_HPP
#define TICS_CLAMP_HPP

#include <boost/cstdint.hpp>

namespace tics {
    boost::uint8_t clamp_uint8(int value);
    boost::uint8_t clamp_uint4(int value);
}

#endif
