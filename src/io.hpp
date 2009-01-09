#ifndef TICS_IO_HPP
#define TICS_IO_HPP

#include <iostream>
#include <boost/cstdint.hpp>

namespace tics {
    void read(std::istream &in, boost::uint8_t &value);
    void read(std::istream &in, boost::uint16_t &value);
    void write(std::ostream &out, boost::uint8_t value);
    void write(std::ostream &out, boost::uint16_t value);
}

#endif
