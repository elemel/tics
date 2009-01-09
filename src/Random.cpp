#include "Random.hpp"

namespace tics {
    Random::Random(int seed)
        : generator_(unsigned(seed))
    { }

    bool Random::flip()
    {
        return bool(generator_() % 2);
    }
    
    int Random::sign()
    {
        return flip() ? -1 : 1;
    }

    int Random::range(int last)
    {
        return generator_() % last;
    }
    
    int Random::range(int first, int last)
    {
        return first + generator_() % (last - first);
    }

    int Random::offset(int last)
    {
        return sign() * range(last);
    }
    
    int Random::offset(int first, int last)
    {
        return sign() * range(first, last);
    }
}
