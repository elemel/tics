#include "io.hpp"

using boost::uint16_t;
using std::istream;
using std::ostream;

namespace tics {
    void read(std::istream &in, boost::uint8_t &value)
    {
        in.read(reinterpret_cast<char *>(&value), sizeof(value));
    }
    
    void read(istream &in, uint16_t &value)
    {
        in.read(reinterpret_cast<char *>(&value), sizeof(value));
    }

    void write(ostream &out, uint8_t value)
    {
        out.write(reinterpret_cast<const char *>(&value), sizeof(value));
    }

    void write(ostream &out, uint16_t value)
    {
        out.write(reinterpret_cast<const char *>(&value), sizeof(value));
    }
}
