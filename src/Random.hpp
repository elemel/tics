#ifndef TICS_RANDOM_HPP
#define TICS_RANDOM_HPP

#include <boost/random/mersenne_twister.hpp>

namespace tics {
    class Random {
    public:
        explicit Random(int seed);
    
        bool flip();
        int sign();
        int range(int last);
        int range(int first, int last);
        int offset(int last);
        int offset(int first, int last);
    
    private:
        boost::mt19937 generator_;
    };
}

#endif
